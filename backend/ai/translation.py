"""
Helsinki-NLP Translation — English → Indian Languages
Models: opus-mt-en-{lang} series
Size: ~298MB per language pair | Free | Hugging Face

Supported output languages:
    hi → Hindi      bn → Bengali
    ta → Tamil      te → Telugu
    gu → Gujarati   mr → Marathi
"""

import functools
from transformers import MarianMTModel, MarianTokenizer

# Available translation pairs
TRANSLATION_MODELS = {
    "hi": "Helsinki-NLP/opus-mt-en-hi",
    "bn": "Helsinki-NLP/opus-mt-en-bn",
    "ta": "Helsinki-NLP/opus-mt-en-ta",
    "te": "Helsinki-NLP/opus-mt-en-te",
    "gu": "Helsinki-NLP/opus-mt-en-mul",   # multilingual fallback
    "mr": "Helsinki-NLP/opus-mt-en-mul",   # multilingual fallback
}

# Cache loaded models — avoid reloading on every message
_model_cache = {}


def _load_translation_model(lang: str):
    if lang not in _model_cache:
        model_name = TRANSLATION_MODELS.get(lang)
        if not model_name:
            return None, None
        print(f"[AI] Loading Helsinki-NLP translator for '{lang}'...")
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model     = MarianMTModel.from_pretrained(model_name)
        _model_cache[lang] = (tokenizer, model)
    return _model_cache[lang]


def translate(text: str, target_lang: str) -> str:
    """
    Translate English text to target Indian language.
    Falls back to English if language not supported.

    Usage:
        translate("Your grievance has been registered.", "hi")
        → "आपकी शिकायत दर्ज हो गई है।"

        translate("You qualify for PM-KISAN scheme.", "ta")
        → "நீங்கள் PM-KISAN திட்டத்திற்கு தகுதி பெறுகிறீர்கள்."
    """
    if target_lang == "en" or target_lang not in TRANSLATION_MODELS:
        return text                           # no translation needed

    try:
        tokenizer, model = _load_translation_model(target_lang)
        if not tokenizer:
            return text

        inputs  = tokenizer([text], return_tensors="pt", truncation=True, max_length=512)
        outputs = model.generate(**inputs)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    except Exception as e:
        print(f"[AI] Translation error ({target_lang}): {e}")
        return text                           # return English on failure


def translate_message(template: str, lang: str, **kwargs) -> str:
    """
    Fill template with values then translate.

    Usage:
        translate_message(
            "Your ticket {ticket} status is {status}.",
            lang="hi",
            ticket="GRV-1234",
            status="Resolved"
        )
    """
    filled = template.format(**kwargs)
    return translate(filled, lang)
