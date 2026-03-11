"""
Indic Transliteration — Roman Hinglish → Devanagari
Library: indic-transliteration
Size: ~1MB | Free | No model download needed
"""

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


def roman_to_devanagari(text: str) -> str:
    """
    Convert Roman/Hinglish text to Devanagari script.
    Used as preprocessing before IndicBERT embedding.

    Usage:
        roman_to_devanagari("mera ghar")   → "मेरा घर"
        roman_to_devanagari("paani nahi")  → "पानी नहीं"
    """
    try:
        return transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
    except Exception as e:
        print(f"[AI] Transliteration error: {e}")
        return text                            # return original on failure


def preprocess_message(text: str, lang: str) -> str:
    """
    Full preprocessing pipeline:
    - If Hinglish (Roman Hindi) → convert to Devanagari
    - If already Devanagari/other script → return as-is
    - If English → return as-is

    Usage:
        preprocess_message("paani nahi aa raha", "hi")
        → "पानी नहीं आ रहा"
    """
    if lang != "en" and _is_roman_script(text):
        return roman_to_devanagari(text)
    return text


def _is_roman_script(text: str) -> bool:
    """Check if text is written in Roman (Latin) script."""
    roman_chars = sum(1 for c in text if ord(c) < 128 and c.isalpha())
    total_chars = sum(1 for c in text if c.isalpha())
    if total_chars == 0:
        return False
    return (roman_chars / total_chars) > 0.7
