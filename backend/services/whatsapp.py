"""
WhatsApp Cloud API Client
Meta Business Platform — Primary messaging channel
"""

import httpx
import os

WA_TOKEN    = os.getenv("WHATSAPP_TOKEN", "")
WA_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")
WA_API_URL  = f"https://graph.facebook.com/v18.0/{WA_PHONE_ID}/messages"


async def send_whatsapp(to: str, message: str) -> bool:
    """Send WhatsApp text message to a phone number."""
    if not WA_TOKEN or not WA_PHONE_ID:
        print(f"[DEMO] WhatsApp → {to}: {message}")
        return True

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message, "preview_url": False}
    }
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(WA_API_URL, json=payload, headers=headers)
        return resp.status_code == 200
