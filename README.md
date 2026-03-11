# NagarVaani

**Every Citizen Heard. Every Vote Counted. Every Scheme Delivered.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Cloud_API-25D366?style=flat-square&logo=whatsapp)](https://developers.facebook.com/docs/whatsapp)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**India Innovates 2026 · Bharat Mandapam, New Delhi · March 28, 2026**
**Team Code-Scavengers · Indian Institute of Information Technology, Nagpur (IIITN)**

---

## Problem Statement

> *"Develop an AI-Driven Booth Management System that transforms static voter lists into a living Knowledge Graph — enabling hyper-local targeting by categorising every voter at booth level and delivering personalised governance updates directly to their devices."*

India manages **96.8 crore registered voters** across **10.5 lakh polling booths** with zero AI intelligence layer:

- Booth data is static — no segmentation, no personalisation
- 500+ government portals — citizens do not know what they qualify for
- No proactive push communication between government and citizen
- Rural India excluded — no app, no internet, no awareness

---

## Two Core Objectives

### Objective 1 — Intelligent Segmentation
Automatically classify every voter at booth level into segments and identify Key Voters.

```
Segments: Youth · Women · Farmers · Businessmen · Senior Citizens
                          |
             Key Voter Score (max 16 pts)
             Score >= 7  -->  KEY VOTER
```

### Objective 2 — Beneficiary Linkage
Track government scheme beneficiaries per booth, notify unclaimed eligible citizens, and strengthen the leader-citizen bond.

```
Citizen Profile --> 14 Schemes Matched --> Auto-notify --> Mark Claimed --> Booth Coverage Updated
```

---

## Live Demo Output

Both objectives verified with working code.
Full output: [docs/demo_output.txt](docs/demo_output.txt)

```
CITIZEN: Ramesh Kumar  |  28yr · Farmer · OBC · BPL · Nagpur
-------------------------------------------------------------
Objective 1 -- INTELLIGENT SEGMENTATION
  Segments : YOUTH · FARMER
  Score    : 13/16  -->  KEY VOTER
  Breakdown:
    +4  Multi-segment overlap (2 segments)
    +5  Antyodaya / BPL + very low income
    +2  Youth voter (26-35)
    +2  Farmer

Objective 2 -- BENEFICIARY LINKAGE
  Schemes matched: 8
    PM-KISAN              -- Rs.6,000/year direct transfer
    Ayushman Bharat       -- Rs.5 lakh health cover/year
    PM Awas Yojana        -- Rs.1.2 lakh  [Deadline: 31 Mar 2026]
    Kisan Credit Card     -- Credit up to Rs.3 lakh
    Atal Pension Yojana   -- Rs.1,000-5,000/month
    OBC Pre-Matric        -- Rs.7,000/year scholarship
    PM Kisan Drone Yojana -- Rs.5 lakh drone subsidy  [NEW 2026]
    Youth Startup Grant   -- Rs.2 lakh grant  [NEW 2026]

Security:
  Phone stored   : 919876***201  (plain text for WhatsApp lookup)
  Voter ID token : dc0fcf4f8a157ed03ac7...  (SHA-256 one-way hash)
  Aadhaar token  : ae6577d181be96175e4a...  (SHA-256 one-way hash)
  Breach value   : Anonymous tokens only. Zero PII.
```

---

## API Routes

> Interactive API docs available at `http://127.0.0.1:8000/docs` after running the server.

### Base

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Project info — name, tagline, team, status |
| GET | `/health` | Health check — returns `{"status":"ok"}` |

### WhatsApp Webhook

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/webhook/` | Meta webhook verification (required by WhatsApp Cloud API) |
| POST | `/webhook/` | Incoming WhatsApp message handler — routes to registration FSM or feature handler |

**POST /webhook/ — Sample incoming payload:**
```json
{
  "entry": [{
    "changes": [{
      "value": {
        "messages": [{
          "from": "919876543201",
          "text": { "body": "schemes" }
        }]
      }
    }]
  }]
}
```

### Schemes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/schemes/all` | Returns all 14 government schemes with benefit and deadline |
| POST | `/schemes/match` | Match schemes for a citizen profile — returns matched schemes + Key Voter score |

**POST /schemes/match — Sample request:**
```json
{
  "age": 28,
  "gender": "M",
  "income": 45000,
  "occupation": "FARMER",
  "category": "OBC",
  "bpl": true,
  "district": "Nagpur"
}
```

**POST /schemes/match — Sample response:**
```json
{
  "schemes": [
    {
      "id": "S01",
      "title": "PM-KISAN",
      "benefit": "Rs.6,000/year direct transfer",
      "deadline": "Ongoing",
      "apply_link": "https://pmkisan.gov.in"
    }
  ],
  "segmentation": {
    "segments": ["YOUTH", "FARMER"],
    "score": 13,
    "is_key_voter": true,
    "label": "KEY VOTER",
    "breakdown": [
      ["Multi-segment (2)", 4],
      ["Antyodaya / BPL + very low income", 5],
      ["Youth voter (26-35)", 2],
      ["Farmer", 2]
    ]
  }
}
```

### Grievance

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/grievance/all` | Returns all grievances — for admin dashboard |
| POST | `/grievance/update` | Update grievance status — called by government officer |

**POST /grievance/update — Sample request:**
```json
{
  "ticket_id": "GRV-1234",
  "status": "IN_PROGRESS",
  "officer": "Suresh_Kumar"
}
```

**Grievance status values:** `OPEN` → `IN_PROGRESS` → `RESOLVED`

---

## System Architecture

```
+------------------------------------------------------------------+
|  INTERFACE     -->  Citizen (WhatsApp User)                      |
|                -->  WhatsApp Cloud API (Meta) -- Primary Channel |
+------------------------------------------------------------------+
|  API LAYER     -->  FastAPI + Uvicorn                            |
|                -->  Request Router + Duplicate Check             |
+------------------------------------------------------------------+
|  AI ENGINE     -->  XLM-RoBERTa    (Language Detection)         |
|                -->  indic-translit  (Hinglish to Devanagari)    |
|                -->  IndicBERT v2   (768-dim Semantic Embedding)  |
|                -->  Intent Classifier (Cosine Similarity)        |
|                     SCHEME / GRIEVANCE / STATUS / GREET         |
+------------------------------------------------------------------+
|  SERVICES      -->  Scheme Matcher  (SQL + pgvector)             |
|                -->  Grievance Engine (Auto-route to officer)     |
|                -->  Ticket Generator (GRV-XXXX)                  |
|                -->  Notification System (Celery async)           |
+------------------------------------------------------------------+
|  DATA LAYER    -->  Supabase (PostgreSQL 15 + pgvector)         |
|                -->  Users DB (SHA-256 tokens only)               |
|                -->  Schemes DB (14 government schemes)           |
+------------------------------------------------------------------+
|  CACHE/TASKS   -->  Upstash Redis (Session FSM + OTP TTL)       |
|                -->  Celery Workers (Async notifications)         |
|                -->  Celery Beat (Scheme deadline alerts 30d)     |
+------------------------------------------------------------------+
|  INFRA         -->  ngrok + local laptop (demo)                  |
|                -->  Admin Dashboard -- React 18 + Tailwind       |
|                -->  AES-256 + TLS 1.3 + SHA-256                 |
+------------------------------------------------------------------+
```

---

## AI Pipeline -- 4 Models

| Step | Model | Purpose | Size |
|------|-------|---------|------|
| 1 | XLM-RoBERTa (`papluca/xlm-roberta-base-language-detection`) | Detect language — 24 languages (23 Indic + English) | 278MB |
| 2 | indic-transliteration (library) | Roman Hinglish to Devanagari — "paani nahi" to Devanagari | ~1MB |
| 3 | IndicBERT v2 (`ai4bharat/IndicBERTv2-MLM-only`) | 768-dim semantic embedding + intent classification | 472MB |
| 4 | Helsinki-NLP opus-mt (en-hi, en-bn, en-ta, en-te, en-gu, en-mr) | Translate response to user preferred language | 298MB each |

**Total: ~1.8GB — runs on free Google Colab T4 GPU**

```
User message (any Indian language / Hinglish)
        |
        v
XLM-RoBERTa  -->  Detect language
        |
        v
indic-transliteration  -->  Roman Hinglish to Devanagari
        |
        v
IndicBERT v2  -->  768-dim embedding + intent classification
        |
        v
   +----+----+
   |         |
SCHEME    GRIEVANCE
PATH      PATH
pgvector  PostgreSQL
cosine    GRV-XXXX
search    ticket
   |         |
   +----+----+
        |
        v
Helsinki-NLP  -->  Translate to user language
        |
        v
WhatsApp Cloud API  -->  Deliver to citizen
```

---

## Key Voter Scoring (Max 16 pts)

| Factor | Points |
|--------|--------|
| 3+ segment overlap | +6 |
| 2 segment overlap | +4 |
| Antyodaya card / BPL + very low income | +5 |
| BPL card | +3 |
| Age 18-25 (first-time voter) | +3 |
| Age 26-35 | +2 |
| Female voter | +2 |
| Farmer | +2 |
| Daily wage worker | +3 |
| Businessperson | +2 |
| **Score >= 7 = KEY VOTER** | **Max: 16** |

---

## Various Government Schemes

| ID | Scheme | Benefit | Deadline |
|----|--------|---------|----------|
| S01 | PM-KISAN | Rs.6,000/year direct transfer | Ongoing |
| S02 | Ayushman Bharat (PM-JAY) | Rs.5 lakh health cover/year | Ongoing |
| S03 | Ujjwala Yojana | Free LPG connection | Ongoing |
| S04 | PM Awas Yojana (Rural) | Rs.1.2 lakh housing subsidy | 31 Mar 2026 |
| S05 | PM Scholarship Scheme | Rs.10,000/year | Ongoing |
| S06 | PM Mudra Yojana | Business loan up to Rs.10 lakh | Ongoing |
| S07 | Kisan Credit Card | Credit up to Rs.3 lakh | Ongoing |
| S08 | Atal Pension Yojana | Rs.1,000-5,000 pension/month | Ongoing |
| S09 | PM Kisan Drone Yojana (NEW) | Rs.5 lakh drone subsidy | 30 Jun 2026 |
| S10 | Digital Sakhi Yojana (NEW) | Rs.15,000 digital skills training | 30 Apr 2026 |
| S11 | Youth Startup Grant 2026 (NEW) | Rs.2 lakh grant | 15 May 2026 |
| S12 | SC/ST Scholarship | Rs.12,000/year | Ongoing |
| S13 | OBC Pre-Matric Scholarship | Rs.7,000/year | Ongoing |
| S14 | Senior Citizen Welfare Scheme | Rs.2,000/month pension | Ongoing |

---

## Tech Stack

| Layer | Technology | Version | Cost |
|-------|-----------|---------|------|
| Backend API | FastAPI + Uvicorn | 0.110 / 0.29 | Free |
| Database | Supabase (PostgreSQL 15 + pgvector) | PostgreSQL 15 | Free |
| Session / Cache | Upstash Redis | Latest | Free (10k req/day) |
| Task Queue | Celery + Celery Beat | 5.3.x | Free |
| AI -- Language Detection | XLM-RoBERTa (`papluca`) | Base | Free |
| AI -- NLP + Embeddings | IndicBERT v2 (`ai4bharat`) | v2 | Free |
| AI -- Translation | Helsinki-NLP opus-mt series | Latest | Free |
| AI -- Transliteration | indic-transliteration | 2.3.45 | Free |
| AI -- OCR | EasyOCR (offline, no API key) | 1.7.1 | Free |
| Messaging -- Primary | Meta WhatsApp Cloud API | v18.0 | Free (1000 conv/month) |
| Messaging -- Fallback | Twilio SMS | Latest | Free (trial credit) |
| Security | AES-256 + TLS 1.3 + SHA-256 | -- | Free |
| Admin Dashboard | React 18 + Tailwind CSS + Vercel | React 18 | Free |
| Demo Hosting | ngrok + local laptop | Latest | Free |
| CI/CD | GitHub Actions | -- | Free |
| **Total Cost** | | | **Rs.0** |

---

## Security Model -- DPDP Act 2023 Compliant

| Data Field | How Stored | Reason |
|-----------|-----------|--------|
| Phone number | Plain text | Required for WhatsApp lookup and reply |
| Voter ID | SHA-256 one-way hash | PII -- Aadhaar Act 2016 |
| Aadhaar number | SHA-256 one-way hash | PII -- DPDP Act 2023 |
| OTP | Upstash Redis TTL 5 min, max 3 attempts | Never persisted in database |
| All database fields | AES-256 encryption at rest | Supabase built-in encryption |
| All data in transit | TLS 1.3 | HTTPS enforced on all endpoints |

**Breach Uselessness Design** -- If the system is hacked, the attacker gets a list of anonymous SHA-256 tokens mapped to ward numbers. No names, phone numbers, Aadhaar numbers, or addresses are ever stored.

---

## WhatsApp Conversation Flow (Redis FSM)

```
New User:
  START --> LANG --> AGE --> GENDER --> INCOME --> CATEGORY --> DISTRICT --> BPL --> DONE
                                                                               |
                                                        Scheme matching runs automatically
                                                        Key Voter score calculated
                                                        Results sent in user language

Returning User (phone unchanged):
  Message --> is_registered(phone) = YES --> Route to SCHEME / GRIEVANCE / STATUS

Re-registration (lost phone / SIM change):
  AWAITING_AADHAAR --> SHA-256 hash lookup --> Found --> OTP sent via WhatsApp
  AWAITING_OTP --> Verified --> Profile transferred to new phone --> Audit log created
```

---

## Database Schema

```sql
-- Users (phone plain for lookup, all PII as SHA-256 tokens)
users: phone (PK), language, district, age, gender, income,
       category, occupation, bpl, voter_token (SHA-256),
       aadhaar_token (SHA-256), is_active, created_at

-- Government Schemes
schemes: scheme_id (PK), title_en, title_hi, description,
         benefit, deadline, apply_link, min_age, max_age,
         max_income, gender, bpl_required, category[], district

-- Scheme vector embeddings for pgvector semantic search
scheme_embeddings: scheme_id (FK), embedding VECTOR(768)

-- Grievances
grievances: ticket_id (PK), phone (FK), description, category,
            status (OPEN / IN_PROGRESS / RESOLVED),
            assigned_to, created_at, resolved_at

-- Re-registration audit log
re_registration_log: id, old_phone, new_phone, method, verified_at
```

---

## Project Structure

```
nagarvaani/
├── demo.py                        <-- Run this for live demonstration
├── test_core.py                   <-- Verify Objective 1 + Objective 2
├── test_ai_pipeline.py            <-- Test all 4 BERT models
├── requirements.txt
├── .env.example
├── backend/
│   ├── main.py                    <-- FastAPI application entry point
│   ├── ai/
│   │   ├── language_detect.py     <-- XLM-RoBERTa language detection
│   │   ├── transliterate.py       <-- Hinglish to Devanagari
│   │   ├── embeddings.py          <-- IndicBERT v2 + intent classification
│   │   ├── translation.py         <-- Helsinki-NLP translation
│   │   └── pipeline.py            <-- Full AI pipeline (all 4 connected)
│   ├── routes/
│   │   ├── webhook.py             <-- WhatsApp webhook + FSM registration
│   │   ├── schemes.py             <-- Scheme matching API routes
│   │   └── grievance.py           <-- Grievance tracking API routes
│   ├── models/
│   │   ├── user.py                <-- User DB model + SHA-256 tokenisation
│   │   └── grievance.py           <-- Grievance model + GRV-XXXX tickets
│   ├── services/
│   │   ├── scheme_matcher.py      <-- 14 schemes eligibility engine
│   │   ├── segmentation.py        <-- Key Voter scoring (Objective 1)
│   │   ├── notifications.py       <-- Celery async WhatsApp notifications
│   │   └── whatsapp.py            <-- Meta WhatsApp Cloud API client
│   └── utils/
│       ├── security.py            <-- SHA-256 hashing + AES-256
│       └── flow_manager.py        <-- Upstash Redis FSM state manager
├── database/
│   ├── schema.sql                 <-- Full PostgreSQL + pgvector schema
│   └── seed_data.sql              <-- 20 mock citizens across 2 booths
└── docs/
    ├── architecture.md            <-- Detailed architecture documentation
    └── demo_output.txt            <-- Live verified demo output
```

---

## Quick Start

```bash
# Clone repository
git clone https://github.com/Palakdeep-Singh/nagarvaani.git
cd nagarvaani

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run live demo (no external setup needed)
python demo.py

# Start API server
uvicorn backend.main:app --reload --port 8000

# Open interactive API docs
# http://127.0.0.1:8000/docs
```

---

## Why NagarVaani

| Feature | MyGov / UMANG | NagarVaani |
|---------|--------------|------------|
| Push to citizen | No | Yes |
| Booth-level intelligence | No | Yes |
| Scheme auto-match | No | Yes |
| Regional language support | Partial | Yes |
| No app download needed | No | Yes -- WhatsApp only |
| Grievance tracking | No | Yes |
| Works on 2G networks | No | Yes |
| Zero PII stored | No | Yes |
| Key Voter identification | No | Yes |
| Auto scheme deadline alerts | No | Yes |

---

## Impact

| Metric | Value |
|--------|-------|
| Eligible Voters | 90 Crore |
| Polling Booths | 10.5 Lakh |
| Languages Supported | 24 (23 Indic + English) |
| Government Schemes | 14 Central Schemes |
| Minimum Connectivity | 2G+ |
| App Download Required | None |
| PII Stored | Zero |
| Total Cost | Rs.0 |

---

## Team -- Code-Scavengers

| Name | Role |
|------|------|
| Palakdeep  | Team Lead · AI/ML Pipeline · IndicBERT + XLM-RoBERTa Integration |
| Prakarsh Jain | Backend Development · FastAPI + WhatsApp Webhook · Redis FSM |
| Yash Yadav | Database Architecture · PostgreSQL + pgvector · Security Model |
| Utkarsh Singh | Scheme Eligibility Engine · Key Voter Scoring · Data Layer |
| Nikhil Bhati | Admin Dashboard · React + Tailwind · Celery Notifications |
| Vivek Singh | WhatsApp Integration · Testing · Deployment · ngrok Setup |

**Institution:** Indian Institute of Information Technology, Nagpur (IIITN)
**Event:** India Innovates 2026 · Bharat Mandapam · New Delhi · March 28, 2026

---

## License

MIT License -- see [LICENSE](LICENSE)