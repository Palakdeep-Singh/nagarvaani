"""
IndicBERT v2 — Semantic Embeddings + Intent Classification
Model: ai4bharat/IndicBERTv2-MLM-only
Size: ~472MB | Free | Hugging Face
Outputs: 768-dimensional float vectors
Supports: 24 languages (23 Indic + English)
"""

import functools
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

MODEL_NAME = "ai4bharat/IndicBERTv2-MLM-only"

# Intent templates — zero-shot classification via cosine similarity
INTENT_TEMPLATES = {
    "SCHEME_QUERY":    "scheme yojana benefit eligibility apply government help subsidy",
    "GRIEVANCE_FILE":  "problem complaint issue broken not working pareshani shikayat",
    "STATUS_CHECK":    "status check ticket update track progress GRV",
    "RE_REGISTER":     "phone changed new number SIM lost register again",
    "GREET":           "hello hi namaste help menu start",
}


@functools.lru_cache(maxsize=1)
def _load_model():
    """Load IndicBERT v2 once, cache in memory."""
    print("[AI] Loading IndicBERT v2...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model     = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()
    return tokenizer, model


def get_embedding(text: str) -> np.ndarray:
    """
    Generate 768-dim semantic embedding for input text.
    Used for: scheme matching (pgvector cosine search) + intent classification.

    Usage:
        vec = get_embedding("mera ration card nahi bana")
        # Returns numpy array of shape (768,)
    """
    tokenizer, model = _load_model()
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=256,
        padding=True
    )
    with torch.no_grad():
        outputs = model(**inputs)

    # Mean pooling over token embeddings
    token_embeddings = outputs.last_hidden_state
    attention_mask   = inputs["attention_mask"]
    mask_expanded    = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    embedding        = (token_embeddings * mask_expanded).sum(1) / mask_expanded.sum(1)

    return embedding[0].numpy()


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def classify_intent(text: str) -> dict:
    """
    Classify user message intent using cosine similarity
    against pre-defined intent templates.

    Returns:
        {
            "intent": "SCHEME_QUERY",
            "confidence": 0.87,
            "all_scores": {...}
        }

    Usage:
        classify_intent("PM Kisan ke liye kaise apply karein")
        → {"intent": "SCHEME_QUERY", "confidence": 0.89}

        classify_intent("paani nahi aa raha 3 din se")
        → {"intent": "GRIEVANCE_FILE", "confidence": 0.91}
    """
    user_embedding = get_embedding(text)

    scores = {}
    for intent, template in INTENT_TEMPLATES.items():
        template_embedding = get_embedding(template)
        scores[intent]     = cosine_similarity(user_embedding, template_embedding)

    best_intent = max(scores, key=scores.get)
    return {
        "intent":     best_intent,
        "confidence": round(scores[best_intent], 4),
        "all_scores": {k: round(v, 4) for k, v in scores.items()}
    }
