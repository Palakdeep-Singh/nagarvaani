"""
NagarVaani — Full AI Message Processing Pipeline
Connects all 4 models in sequence:

User message
    → XLM-RoBERTa   (detect language)
    → indic-translit (Hinglish → Devanagari)
    → IndicBERT v2   (768-dim embedding + intent)
    → Helsinki-NLP   (translate response)
"""

from backend.ai.language_detect import detect_language
from backend.ai.transliterate   import preprocess_message
from backend.ai.embeddings      import classify_intent, get_embedding
from backend.ai.translation     import translate


def process_message(text: str) -> dict:
    """
    Full AI pipeline for incoming WhatsApp message.

    Returns:
        {
            "original":    "paani nahi aa raha",
            "language":    "hi",
            "processed":   "पानी नहीं आ रहा",
            "intent":      "GRIEVANCE_FILE",
            "confidence":  0.91,
            "embedding":   [0.23, -0.14, ...]   # 768-dim
        }
    """
    # Step 1 — Detect language (XLM-RoBERTa)
    lang = detect_language(text)

    # Step 2 — Transliterate if Hinglish (indic-transliteration)
    processed = preprocess_message(text, lang)

    # Step 3 — Classify intent (IndicBERT v2 + cosine similarity)
    intent_result = classify_intent(processed)

    # Step 4 — Get semantic embedding for scheme matching
    embedding = get_embedding(processed)

    return {
        "original":   text,
        "language":   lang,
        "processed":  processed,
        "intent":     intent_result["intent"],
        "confidence": intent_result["confidence"],
        "embedding":  embedding.tolist(),        # for pgvector storage
    }


def build_response(template: str, lang: str, **kwargs) -> str:
    """
    Build and translate response for citizen.

    Usage:
        build_response(
            "Your grievance {ticket} has been registered.",
            lang="hi",
            ticket="GRV-1234"
        )
        → "आपकी शिकायत GRV-1234 दर्ज हो गई है।"
    """
    return translate(template.format(**kwargs), lang)
