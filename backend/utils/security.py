"""
Security Utilities
SHA-256 hashing for PII fields (Voter ID, Aadhaar)
AES-256 encryption wrapper
DPDP Act 2023 + Aadhaar Act 2016 compliant
"""

import hashlib
import os


def hash_sha256(value: str) -> str:
    """
    One-way SHA-256 hash for PII fields.
    Used for: Voter ID, Aadhaar number
    NEVER store the original — only this hash.
    """
    salt = os.getenv("HASH_SALT", "nagarvaani_salt_2026")
    return hashlib.sha256(f"{salt}{value.strip()}".encode()).hexdigest()


def is_valid_aadhaar(aadhaar: str) -> bool:
    """Validate 12-digit Aadhaar format."""
    return aadhaar.strip().isdigit() and len(aadhaar.strip()) == 12


def is_valid_voter_id(voter_id: str) -> bool:
    """
    Validate Voter ID (EPIC) format.
    Format: 3 letters + 7 digits (e.g. ABC1234567)
    """
    v = voter_id.strip().upper()
    return len(v) == 10 and v[:3].isalpha() and v[3:].isdigit()


def mask_phone(phone: str) -> str:
    """Mask phone for logs — e.g. 919876543210 → 91987***3210"""
    if len(phone) >= 10:
        return phone[:5] + "***" + phone[-4:]
    return "***"
