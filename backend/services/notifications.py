"""
Celery Notification Tasks
- Grievance status change → notify citizen via WhatsApp
- Scheme deadline alerts (30 days before expiry)
- Celery Beat schedules daily scheme check
"""

import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.getenv("UPSTASH_REDIS_URL", "redis://localhost:6379")

celery_app = Celery(
    "nagarvaani",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.beat_schedule = {
    # Run every day at 9 AM — check scheme deadlines
    "daily-scheme-alerts": {
        "task":     "backend.services.notifications.send_deadline_alerts",
        "schedule": crontab(hour=9, minute=0),
    },
}


@celery_app.task
def notify_grievance_update(phone: str, ticket_id: str, status: str, lang: str = "en"):
    """
    Called when officer updates grievance status.
    Sends WhatsApp notification to citizen automatically.
    """
    import asyncio
    from backend.services.whatsapp import send_whatsapp
    from backend.ai.translation import translate

    status_messages = {
        "IN_PROGRESS": f"🔄 Your grievance *{ticket_id}* is now being worked on by the assigned officer.",
        "RESOLVED":    f"✅ Your grievance *{ticket_id}* has been resolved. Thank you for your patience.",
        "OPEN":        f"📋 Your grievance *{ticket_id}* has been received and will be assigned shortly.",
    }

    msg = status_messages.get(status, f"Update on {ticket_id}: {status}")
    if lang != "en":
        msg = translate(msg, lang)

    asyncio.run(send_whatsapp(phone, msg))


@celery_app.task
def send_deadline_alerts():
    """
    Daily job — find schemes expiring within 30 days.
    Notify all eligible unclaimed citizens.
    """
    from datetime import datetime, timedelta
    from backend.services.scheme_matcher import SCHEMES
    from backend.models.user import _conn
    from backend.services.whatsapp import send_whatsapp
    import asyncio

    today    = datetime.today()
    soon     = today + timedelta(days=30)
    notified = 0

    for scheme in SCHEMES:
        deadline_str = scheme.get("deadline", "Ongoing")
        if deadline_str == "Ongoing":
            continue
        try:
            deadline = datetime.strptime(deadline_str, "%d %b %Y")
            if today <= deadline <= soon:
                # Fetch all eligible users and notify
                with _conn() as c:
                    users = c.execute("SELECT phone, language FROM users WHERE is_active=1").fetchall()
                for phone, lang in users:
                    msg = (
                        f"⚠️ *Deadline Alert!*\n"
                        f"*{scheme['title']}* deadline is {deadline_str}.\n"
                        f"Benefit: {scheme['benefit']}\n"
                        f"Apply: {scheme['apply_link']}"
                    )
                    asyncio.run(send_whatsapp(phone, msg))
                    notified += 1
        except ValueError:
            continue

    return f"Deadline alerts sent: {notified}"
