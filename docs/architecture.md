# NagarVaani — Architecture Documentation

## System Overview

NagarVaani is a WhatsApp-first AI civic platform built for India Innovates 2026.
It addresses two core objectives:

1. **Intelligent Segmentation** — Auto-classify booth voter data into Youth, Women, Farmers, Businessmen, Senior Citizens and identify Key Voters
2. **Beneficiary Linkage** — Track government scheme beneficiaries at booth level

---

## Message Processing Pipeline

```
User (WhatsApp) → Meta Cloud API → FastAPI Webhook
    → XLM-RoBERTa (language detect)
    → indic-transliteration (Hinglish → Devanagari)
    → IndicBERT v2 (768-dim embedding)
    → Intent Classifier (cosine similarity)
        → SCHEME: pgvector cosine search → ranked results
        → GRIEVANCE: PostgreSQL → GRV-XXXX ticket → officer alert
    → Helsinki-NLP (translate to user language)
    → WhatsApp reply
```

## Key Voter Score

Maximum 16 points. Score ≥ 7 = KEY VOTER 🔑

| Factor | Points |
|--------|--------|
| 3+ segments | +6 |
| 2 segments | +4 |
| Antyodaya/BPL + low income | +5 |
| BPL card | +3 |
| Age 18–25 | +3 |
| Age 26–35 | +2 |
| Female | +2 |
| Farmer | +2 |
| Daily wage | +3 |
| Businessperson | +2 |

## Security

- Phone: plain text (WhatsApp lookup)
- Voter ID: SHA-256 hash only
- Aadhaar: SHA-256 hash only
- OTP: Redis TTL 5 min, max 3 attempts, never in DB
- DB at rest: AES-256 (Supabase)
- Transit: TLS 1.3

**Breach uselessness**: If hacked, attacker gets anonymous tokens + ward numbers. Zero PII.
