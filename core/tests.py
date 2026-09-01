import os
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from core.models import Box, BoxCategory, Product
from core.services.ai_classifier import classify_product_category


class BoxRecommendationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Box.objects.create(
            name="Standard Small",
            length=20,
            width=15,
            height=10,
            max_weight=5,
            cost=15.00,
            allowed_categories=[BoxCategory.STANDARD, BoxCategory.APPAREL],
        )
        Box.objects.create(
            name="Fragile Large",
            length=25,
            width=20,
            height=15,
            max_weight=10,
            cost=30.00,
            allowed_categories=[BoxCategory.FRAGILE, BoxCategory.LIQUID],
        )

    def test_product_category_uses_gemini_when_available(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=False):
            with patch("core.services.ai_classifier.call_gemini_for_category", return_value=BoxCategory.FRAGILE):
                self.assertEqual(classify_product_category("Glass bottle", "fragile"), BoxCategory.FRAGILE)

    def test_product_category_falls_back_to_standard(self):
        self.assertEqual(classify_product_category("random product"), BoxCategory.STANDARD)

    def test_create_product_with_manual_category(self):
        response = self.client.post(
            "/api/v1/products/",
            {
                "title": "Glass mug",
                "description": "Fragile item",
                "length": 8,
                "width": 8,
                "height": 12,
                "weight": 1,
                "category": BoxCategory.FRAGILE,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.get().category, BoxCategory.FRAGILE)

    def test_recommend_box_uses_lowest_cost_compatible_option(self):
        payload = {
            "items": [
                {
                    "title": "T-shirt",
                    "length": 12,
                    "width": 10,
                    "height": 4,
                    "weight": 0.5,
                    "category": BoxCategory.APPAREL,
                    "quantity": 1,
                }
            ]
        }
        response = self.client.post("/api/v1/recommend-box/", payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["box_name"], "Standard Small")
