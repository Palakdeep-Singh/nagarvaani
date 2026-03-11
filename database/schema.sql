-- NagarVaani Database Schema
-- PostgreSQL 15 + pgvector (Supabase)
-- DPDP Act 2023 + Aadhaar Act 2016 compliant

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Citizens table
-- phone stored PLAIN for WhatsApp lookup
-- all PII stored as SHA-256 tokens only
CREATE TABLE users (
    phone          TEXT PRIMARY KEY,               -- plain for lookup
    language       TEXT DEFAULT 'en',
    district       TEXT,
    age            INTEGER,
    income         INTEGER,
    gender         TEXT,                           -- M / F / O
    category       TEXT,                           -- GEN / OBC / SC / ST
    occupation     TEXT,                           -- FARMER / STUDENT etc.
    bpl            BOOLEAN DEFAULT FALSE,
    voter_token    TEXT UNIQUE,                    -- SHA-256(voter_id)
    aadhaar_token  TEXT UNIQUE,                    -- SHA-256(aadhaar)
    is_active      BOOLEAN DEFAULT TRUE,
    created_at     TIMESTAMP DEFAULT NOW(),
    updated_at     TIMESTAMP DEFAULT NOW()
);

-- Government Schemes (14 central schemes)
CREATE TABLE schemes (
    scheme_id      TEXT PRIMARY KEY,               -- S01, S02...
    title_en       TEXT NOT NULL,
    title_hi       TEXT,
    description_en TEXT,
    benefit        TEXT,
    deadline       TEXT,
    apply_link     TEXT,
    min_age        INTEGER DEFAULT 0,
    max_age        INTEGER DEFAULT 100,
    max_income     INTEGER DEFAULT 999999,
    gender         TEXT DEFAULT 'ANY',             -- M / F / ANY
    bpl_required   BOOLEAN DEFAULT FALSE,
    category       TEXT[] DEFAULT '{}',            -- GEN/OBC/SC/ST
    district       TEXT DEFAULT 'ALL',
    is_active      BOOLEAN DEFAULT TRUE,
    created_at     TIMESTAMP DEFAULT NOW()
);

-- Scheme vector embeddings for semantic matching
CREATE TABLE scheme_embeddings (
    scheme_id  TEXT REFERENCES schemes(scheme_id),
    embedding  VECTOR(768),                        -- IndicBERT v2 output
    created_at TIMESTAMP DEFAULT NOW()
);

-- Grievances
CREATE TABLE grievances (
    ticket_id    TEXT PRIMARY KEY,                 -- GRV-XXXX
    phone        TEXT REFERENCES users(phone),
    description  TEXT NOT NULL,
    category     TEXT DEFAULT 'GENERAL',
    status       TEXT DEFAULT 'OPEN',              -- OPEN/IN_PROGRESS/RESOLVED
    assigned_to  TEXT,
    created_at   TIMESTAMP DEFAULT NOW(),
    resolved_at  TIMESTAMP
);

-- Re-registration audit log
CREATE TABLE re_registration_log (
    id          SERIAL PRIMARY KEY,
    old_phone   TEXT,
    new_phone   TEXT,
    method      TEXT DEFAULT 'aadhaar_otp',
    verified_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_users_district   ON users(district);
CREATE INDEX idx_grievances_phone ON grievances(phone);
CREATE INDEX idx_grievances_status ON grievances(status);
CREATE INDEX idx_scheme_emb       ON scheme_embeddings
    USING ivfflat (embedding vector_cosine_ops);
