from fastapi import APIRouter, Request, HTTPException
from backend.services.whatsapp import send_whatsapp
from backend.services.scheme_matcher import match_schemes
from backend.services.segmentation import calculate_key_voter_score
from backend.utils.flow_manager import FlowManager
from backend.utils.security import hash_sha256
from backend.models.user import get_user, create_user, is_registered
from backend.models.grievance import create_grievance, get_grievance_status
import os

router = APIRouter()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "nagarvaani_2026")

# ── Webhook verification (Meta requirement) ──────────────────────────────────
@router.get("/")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    if (params.get("hub.mode") == "subscribe" and
            params.get("hub.verify_token") == VERIFY_TOKEN):
        return int(params["hub.challenge"])
    raise HTTPException(status_code=403, detail="Verification failed")


# ── Incoming message handler ─────────────────────────────────────────────────
@router.post("/")
async def handle_webhook(request: Request):
    body = await request.json()
    try:
        entry   = body["entry"][0]
        changes = entry["changes"][0]
        value   = changes["value"]
        message = value["messages"][0]

        phone = message["from"]
        text  = message.get("text", {}).get("body", "").strip()

        if not text:
            return {"status": "ignored"}

        # Duplicate / re-registration check
        if is_registered(phone):
            await handle_registered_user(phone, text)
        else:
            await handle_new_user(phone, text)

    except (KeyError, IndexError):
        pass  # Status updates, read receipts — ignore

    return {"status": "ok"}


# ── Registered user — route to features ──────────────────────────────────────
async def handle_registered_user(phone: str, text: str):
    user = get_user(phone)
    lang = user.get("language", "en")
    t    = text.lower().strip()

    if t in ["schemes", "yojana", "योजना"]:
        matched = match_schemes(user)
        if matched:
            msg = "📋 *Your eligible schemes:*\n\n"
            for s in matched:
                msg += f"✅ *{s['title']}*\n"
                msg += f"   Benefit: {s['benefit']}\n"
                msg += f"   Deadline: {s['deadline']}\n"
                msg += f"   Apply: {s['apply_link']}\n\n"
        else:
            msg = "No schemes found for your profile right now."

    elif t.startswith("grievance ") or t.startswith("shikayat "):
        desc   = text[10:].strip()
        ticket = create_grievance(phone, desc)
        msg    = f"✅ Grievance registered!\nTicket ID: *{ticket}*\nType *status {ticket}* to track."

    elif t.startswith("status "):
        ticket_id = text.split()[1].upper()
        status    = get_grievance_status(ticket_id)
        msg       = f"🎫 *{ticket_id}*\nStatus: *{status}*" if status else f"Ticket {ticket_id} not found."

    else:
        msg = (
            "👋 *NagarVaani Menu*\n\n"
            "• *schemes* — view your eligible schemes\n"
            "• *grievance <your issue>* — file a complaint\n"
            "• *status <TICKET_ID>* — track grievance"
        )

    await send_whatsapp(phone, msg)


# ── New user — multi-step registration FSM ───────────────────────────────────
QUESTIONS = {
    "LANG":        "🌐 Select language:\n1. English\n2. Hindi\n3. Hinglish",
    "AGE":         "📅 Enter your age:",
    "GENDER":      "👤 Gender?\n1. Male\n2. Female\n3. Other",
    "INCOME":      "💰 Annual income (in ₹):",
    "CATEGORY":    "📋 Category?\n1. General\n2. OBC\n3. SC\n4. ST",
    "DISTRICT":    "📍 Enter your district:",
    "BPL":         "🪪 Do you have a BPL/Ration card?\n1. Yes (Yellow)\n2. Yes (White)\n3. No",
    "OCCUPATION":  "💼 Occupation?\n1. Farmer\n2. Student\n3. Business\n4. Daily Wage\n5. Other",
}

LANG_MAP = {"1": "en", "2": "hi", "3": "hi", "english": "en", "hindi": "hi", "hinglish": "hi"}
STEPS    = ["LANG", "AGE", "GENDER", "INCOME", "CATEGORY", "DISTRICT", "BPL", "OCCUPATION"]

async def handle_new_user(phone: str, text: str):
    state = FlowManager.get_state(phone) or {}
    step  = state.get("step", "START")
    data  = state.get("data", {})

    if step == "START":
        FlowManager.set_state(phone, {"step": "LANG", "data": {}})
        await send_whatsapp(phone,
            "👋 Welcome to *NagarVaani — नगरवाणी*!\n"
            "AI-powered civic platform for every Indian.\n\n"
            + QUESTIONS["LANG"]
        )
        return

    if step == "EXISTING_AADHAAR":
        await _handle_rereg_aadhaar(phone, text, data)
        return

    if step == "EXISTING_OTP":
        await _handle_rereg_otp(phone, text, data)
        return

    # Process current step answer
    data = _save_step(step, text, data)
    next_step = _get_next_step(step)

    if next_step == "DONE":
        create_user(phone, data)
        matched = match_schemes(data)
        score   = calculate_key_voter_score(data)

        msg = f"✅ *Registration complete!*\n"
        msg += f"Key Voter Score: *{score['score']}/16*"
        if score["is_key_voter"]:
            msg += " 🔑 KEY VOTER"
        msg += f"\n\n📋 *{len(matched)} schemes found for you:*\n\n"
        for s in matched[:5]:
            msg += f"• *{s['title']}* — {s['benefit']}\n"
        msg += "\nType *schemes* anytime to see full list."
        FlowManager.clear_state(phone)
    else:
        FlowManager.set_state(phone, {"step": next_step, "data": data})
        msg = QUESTIONS[next_step]

    await send_whatsapp(phone, msg)


def _save_step(step: str, text: str, data: dict) -> dict:
    mapping = {
        "LANG":       ("language",   lambda t: LANG_MAP.get(t.lower(), "en")),
        "AGE":        ("age",        lambda t: int(t) if t.isdigit() else 25),
        "GENDER":     ("gender",     lambda t: {"1":"M","2":"F","3":"O"}.get(t, "M")),
        "INCOME":     ("income",     lambda t: int(t.replace(",","").replace("₹","")) if t.replace(",","").replace("₹","").isdigit() else 50000),
        "CATEGORY":   ("category",   lambda t: {"1":"GEN","2":"OBC","3":"SC","4":"ST"}.get(t,"GEN")),
        "DISTRICT":   ("district",   lambda t: t.title()),
        "BPL":        ("bpl",        lambda t: t in ["1","2","yes","haan"]),
        "OCCUPATION": ("occupation", lambda t: {"1":"FARMER","2":"STUDENT","3":"BUSINESS","4":"DAILY_WAGE"}.get(t,"OTHER")),
    }
    if step in mapping:
        key, fn = mapping[step]
        try:
            data[key] = fn(text)
        except Exception:
            pass
    return data


def _get_next_step(current: str) -> str:
    idx = STEPS.index(current) if current in STEPS else -1
    return STEPS[idx + 1] if idx + 1 < len(STEPS) else "DONE"


async def _handle_rereg_aadhaar(phone: str, text: str, data: dict):
    from backend.models.user import find_user_by_aadhaar
    from backend.utils.flow_manager import generate_otp
    user = find_user_by_aadhaar(text)
    if not user:
        await send_whatsapp(phone, "❌ No account found. Type *new* to register.")
        FlowManager.clear_state(phone)
        return
    otp = generate_otp(phone)
    # Demo: send OTP via WhatsApp itself
    await send_whatsapp(phone, f"🔢 Your OTP: *{otp}*\n_(Valid 5 minutes, max 3 attempts)_")
    FlowManager.set_state(phone, {"step": "EXISTING_OTP", "data": {"old_phone": user["phone"]}})


async def _handle_rereg_otp(phone: str, text: str, data: dict):
    from backend.utils.flow_manager import verify_otp
    from backend.models.user import transfer_profile
    if verify_otp(phone, text.strip()):
        transfer_profile(data["old_phone"], phone)
        await send_whatsapp(phone, "✅ *Profile restored!*\nType *schemes* to see your schemes.")
    else:
        await send_whatsapp(phone, "❌ Wrong OTP. Please try again or restart.")
    FlowManager.clear_state(phone)
