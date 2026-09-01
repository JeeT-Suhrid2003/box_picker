import json
import logging
import os
import urllib.error
import urllib.request

from core.models import BoxCategory

logger = logging.getLogger(__name__)

VALID_CATEGORIES = [
    BoxCategory.STANDARD,
    BoxCategory.FRAGILE,
    BoxCategory.APPAREL,
    BoxCategory.HEAVY_DUTY,
    BoxCategory.LIQUID,
]


def call_gemini_for_category(title: str, description: str = "") -> str:
    """Call Gemini to classify a product into a valid box category."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    prompt = (
        "Classify this product into one of the following categories: "
        + ", ".join(VALID_CATEGORIES)
        + ". Return only valid JSON with this exact shape: {\"category\": \"CATEGORY_NAME\"}. "
        + "Product title: " + title + ". Description: " + (description or "")
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "response_mime_type": "application/json",
        },
    }

    # Use a model name that is valid for the Google Generative AI endpoint.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        body = json.loads(response.read().decode("utf-8"))

    text = body["candidates"][0]["content"]["parts"][0]["text"]
    parsed = json.loads(text)
    category = parsed.get("category")
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category returned by Gemini: {category}")
    return category


def classify_product_category(title: str, description: str = "") -> str:
    """Best-effort classification using Gemini. Falls back to STANDARD on any failure."""
    try:
        return call_gemini_for_category(title, description)
    except (RuntimeError, ValueError, urllib.error.URLError, json.JSONDecodeError):
        logger.exception("Gemini category classification failed; fallback to STANDARD")
        return BoxCategory.STANDARD
