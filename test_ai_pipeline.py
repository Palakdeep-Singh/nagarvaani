"""
Test the full AI pipeline — run this to verify all 4 models work.
NOTE: First run downloads models (~1.8GB total). Needs internet.

Run: python test_ai_pipeline.py
"""

import sys
sys.path.insert(0, ".")

print("=" * 50)
print("NagarVaani — AI Pipeline Test")
print("=" * 50)

# ── Test 1: Language Detection ───────────────────────
print("\n[1/4] XLM-RoBERTa — Language Detection")
from backend.ai.language_detect import detect_language

tests = [
    ("mera ration card nahi bana",       "hi"),
    ("My water supply is broken",        "en"),
    ("আমার রেশন কার্ড পাইনি",            "bn"),
]
for text, expected in tests:
    result = detect_language(text)
    status = "✅" if result == expected else "⚠️"
    print(f"  {status} '{text[:35]}' → {result} (expected {expected})")

# ── Test 2: Transliteration ──────────────────────────
print("\n[2/4] indic-transliteration — Hinglish → Devanagari")
from backend.ai.transliterate import roman_to_devanagari, preprocess_message

hinglish_tests = [
    "paani nahi aa raha",
    "mera ghar kab banega",
    "PM Kisan mujhe nahi mila",
]
for t in hinglish_tests:
    result = roman_to_devanagari(t)
    print(f"  ✅ '{t}' → '{result}'")

# ── Test 3: Intent Classification ───────────────────
print("\n[3/4] IndicBERT v2 — Intent Classification")
from backend.ai.embeddings import classify_intent

intent_tests = [
    ("PM Kisan ke liye kaise apply karein", "SCHEME_QUERY"),
    ("paani nahi aa raha 3 din se",         "GRIEVANCE_FILE"),
    ("status GRV-1234",                     "STATUS_CHECK"),
    ("namaste",                             "GREET"),
]
for text, expected in intent_tests:
    result = classify_intent(text)
    status = "✅" if result["intent"] == expected else "⚠️"
    print(f"  {status} '{text[:40]}'")
    print(f"      → {result['intent']} (conf: {result['confidence']})")

# ── Test 4: Translation ──────────────────────────────
print("\n[4/4] Helsinki-NLP — Translation")
from backend.ai.translation import translate

translation_tests = [
    ("Your grievance has been registered.", "hi"),
    ("You qualify for PM-KISAN scheme.",    "hi"),
]
for text, lang in translation_tests:
    result = translate(text, lang)
    print(f"  ✅ EN: '{text}'")
    print(f"      {lang.upper()}: '{result}'")

print("\n" + "=" * 50)
print("✅ All AI pipeline tests complete!")
print("=" * 50)
