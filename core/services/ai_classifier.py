import logging

from core.models import BoxCategory

logger = logging.getLogger(__name__)


def classify_product_category(title: str, description: str = "") -> str:
    """Best-effort classification using Gemini. Falls back to STANDARD on any failure."""
    try:
        # Placeholder implementation to keep this project runnable without external AI keys.
        # In production, call the Gemini API here with structured JSON output.
        normalized = (title + " " + description).lower()
        if any(keyword in normalized for keyword in ["glass", "bottle", "fragile", "ceramic", "lamp"]):
            return BoxCategory.FRAGILE
        if any(keyword in normalized for keyword in ["shirt", "dress", "jeans", "fabric", "cloth", "apparel"]):
            return BoxCategory.APPAREL
        if any(keyword in normalized for keyword in ["machine", "tool", "metal", "motor", "engine", "heavy"]):
            return BoxCategory.HEAVY_DUTY
        if any(keyword in normalized for keyword in ["liquid", "oil", "milk", "juice", "sauce", "bottle"]):
            return BoxCategory.LIQUID
        return BoxCategory.STANDARD
    except Exception:
        logger.exception("Gemini category classification failed; fallback to STANDARD")
        return BoxCategory.STANDARD
