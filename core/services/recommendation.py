from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from core.models import Box, BoxCategory


def _fits_in_box(box: Box, length: float, width: float, height: float) -> bool:
    dims = sorted((float(length), float(width), float(height)))
    box_dims = sorted((float(box.length), float(box.width), float(box.height)))
    return dims[0] <= box_dims[0] and dims[1] <= box_dims[1] and dims[2] <= box_dims[2]


def recommend_box_for_items(items: Iterable[dict]) -> dict:
    """Pick the cheapest compatible box that fits all aggregated item dimensions and category rules."""
    items = list(items)
    if not items:
        raise ValueError("At least one item is required for recommendation")

    total_weight = sum(float(item["weight"]) * int(item.get("quantity", 1)) for item in items)
    max_length = max(float(item["length"]) * int(item.get("quantity", 1)) for item in items)
    max_width = max(float(item["width"]) * int(item.get("quantity", 1)) for item in items)
    max_height = max(float(item["height"]) * int(item.get("quantity", 1)) for item in items)
    categories = {item["category"] for item in items}

    compatible_boxes = []
    for box in Box.objects.all():
        if total_weight > float(box.max_weight):
            continue
        if not set(categories).issubset(set(box.allowed_categories)):
            continue
        if not _fits_in_box(box, max_length, max_width, max_height):
            continue
        compatible_boxes.append(box)

    if not compatible_boxes:
        raise ValueError("No compatible box found for the given items")

    selected = min(compatible_boxes, key=lambda box: Decimal(str(box.cost)))
    return {
        "box_id": selected.id,
        "box_name": selected.name,
        "length": float(selected.length),
        "width": float(selected.width),
        "height": float(selected.height),
        "max_weight": float(selected.max_weight),
        "cost": float(selected.cost),
        "allowed_categories": list(selected.allowed_categories),
        "total_weight": total_weight,
        "required_dimensions": {"length": max_length, "width": max_width, "height": max_height},
    }
