"""
Redis FSM Flow Manager
Manages multi-step WhatsApp registration conversation state
OTP generation and verification with TTL
"""

import json
import random
import os
import redis

# Upstash Redis (free tier — 10k req/day)
_redis = redis.from_url(
    os.getenv("UPSTASH_REDIS_URL", "redis://localhost:6379"),
    decode_responses=True
)

STATE_TTL = 3600   # 1 hour — conversation state
OTP_TTL   = 300    # 5 minutes — OTP expiry


class FlowManager:

    @staticmethod
    def get_state(phone: str):
        raw = _redis.get(f"state:{phone}")
        return json.loads(raw) if raw else None

    @staticmethod
    def set_state(phone: str, state: dict):
        _redis.setex(f"state:{phone}", STATE_TTL, json.dumps(state))

    @staticmethod
    def clear_state(phone: str):
        _redis.delete(f"state:{phone}")


def generate_otp(phone: str) -> str:
    """Generate 6-digit OTP, store in Redis with TTL."""
    otp = str(random.randint(100000, 999999))
    _redis.setex(
        f"otp:{phone}",
        OTP_TTL,
        json.dumps({"otp": otp, "attempts": 0})
    )
    return otp


def verify_otp(phone: str, entered: str) -> bool:
    """Verify OTP — max 3 attempts, auto-expire."""
    raw = _redis.get(f"otp:{phone}")
    if not raw:
        return False

    record = json.loads(raw)
    if record["attempts"] >= 3:
        _redis.delete(f"otp:{phone}")
        return False

    if record["otp"] == entered.strip():
        _redis.delete(f"otp:{phone}")
        return True

    record["attempts"] += 1
    _redis.setex(f"otp:{phone}", OTP_TTL, json.dumps(record))
    return False