"""
Language Detection — XLM-RoBERTa
Model: papluca/xlm-roberta-base-language-detection
Supports: 24 languages (23 Indic + English)
Size: ~278MB | Free | Hugging Face
"""

from transformers import pipeline
import functools

SUPPORTED_LANGUAGES = {
    "hi": "Hindi",     "bn": "Bengali",   "ta": "Tamil",
    "te": "Telugu",    "mr": "Marathi",   "gu": "Gujarati",
    "kn": "Kannada",   "ml": "Malayalam", "pa": "Punjabi",
    "ur": "Urdu",      "or": "Odia",      "as": "Assamese",
    "en": "English",
}

@functools.lru_cache(maxsize=1)
def _load_model():
    """Load model once, cache in memory."""
    print("[AI] Loading XLM-RoBERTa language detector...")
    return pipeline(
        "text-classification",
        model="papluca/xlm-roberta-base-language-detection",
        top_k=3
    )


def detect_language(text: str) -> str:
    """
    Detect language of input text.
    Returns ISO 639-1 language code (e.g. 'hi', 'en', 'ta').

    Usage:
        detect_language("mera ration card nahi bana")  → 'hi'
        detect_language("My name is Ramesh")           → 'en'
        detect_language("என் பெயர் ராமேஷ்")           → 'ta'
    """
    try:
        model   = _load_model()
        results = model(text[:512])           # truncate for speed
        top     = results[0][0]
        lang    = top["label"]
        # Map to supported — default English
        return lang if lang in SUPPORTED_LANGUAGES else "en"
    except Exception as e:
        print(f"[AI] Language detection error: {e}")
        return "en"                           # safe fallback


def get_language_name(code: str) -> str:
    return SUPPORTED_LANGUAGES.get(code, "English")
