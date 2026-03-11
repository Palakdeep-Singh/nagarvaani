-- NagarVaani — Demo Seed Data
-- 20 mock citizens across 2 booths for demonstration
-- Run: psql -U postgres -d nagarvaani -f seed_data.sql

INSERT INTO users (phone, language, district, age, gender, income, category, occupation, bpl, created_at) VALUES
-- Booth 14 — Nagpur Rural
('919876543201', 'hi', 'Nagpur', 28, 'M', 45000,  'OBC', 'FARMER',     TRUE,  NOW()),
('919876543202', 'hi', 'Nagpur', 22, 'F', 30000,  'SC',  'STUDENT',    TRUE,  NOW()),
('919876543203', 'hi', 'Nagpur', 45, 'M', 80000,  'GEN', 'FARMER',     FALSE, NOW()),
('919876543204', 'mr', 'Nagpur', 35, 'F', 25000,  'OBC', 'DAILY_WAGE', TRUE,  NOW()),
('919876543205', 'hi', 'Nagpur', 62, 'M', 20000,  'GEN', 'OTHER',      TRUE,  NOW()),
('919876543206', 'hi', 'Nagpur', 19, 'F', 15000,  'SC',  'STUDENT',    TRUE,  NOW()),
('919876543207', 'hi', 'Nagpur', 38, 'M', 120000, 'GEN', 'BUSINESS',   FALSE, NOW()),
('919876543208', 'hi', 'Nagpur', 55, 'F', 35000,  'OBC', 'FARMER',     TRUE,  NOW()),
('919876543209', 'hi', 'Nagpur', 29, 'M', 60000,  'OBC', 'BUSINESS',   FALSE, NOW()),
('919876543210', 'hi', 'Nagpur', 67, 'F', 18000,  'SC',  'OTHER',      TRUE,  NOW()),
-- Booth 07 — Nagpur Urban
('919876543211', 'en', 'Nagpur', 24, 'M', 90000,  'GEN', 'STUDENT',    FALSE, NOW()),
('919876543212', 'hi', 'Nagpur', 42, 'F', 55000,  'OBC', 'BUSINESS',   FALSE, NOW()),
('919876543213', 'hi', 'Nagpur', 33, 'M', 40000,  'SC',  'DAILY_WAGE', TRUE,  NOW()),
('919876543214', 'hi', 'Nagpur', 71, 'M', 22000,  'GEN', 'OTHER',      TRUE,  NOW()),
('919876543215', 'mr', 'Nagpur', 26, 'F', 35000,  'ST',  'FARMER',     TRUE,  NOW()),
('919876543216', 'hi', 'Nagpur', 48, 'M', 75000,  'GEN', 'BUSINESS',   FALSE, NOW()),
('919876543217', 'hi', 'Nagpur', 20, 'F', 28000,  'OBC', 'STUDENT',    TRUE,  NOW()),
('919876543218', 'hi', 'Nagpur', 36, 'M', 50000,  'SC',  'FARMER',     TRUE,  NOW()),
('919876543219', 'hi', 'Nagpur', 58, 'F', 32000,  'OBC', 'DAILY_WAGE', TRUE,  NOW()),
('919876543220', 'en', 'Nagpur', 31, 'M', 110000, 'GEN', 'BUSINESS',   FALSE, NOW());
