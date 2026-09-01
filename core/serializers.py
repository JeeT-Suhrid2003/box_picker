from rest_framework import serializers

from core.models import Box, BoxCategory, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "length",
            "width",
            "height",
            "weight",
            "category",
        ]


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = [
            "id",
            "name",
            "length",
            "width",
            "height",
            "max_weight",
            "cost",
            "allowed_categories",
            "volume",
        ]


class RecommendationItemSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    length = serializers.FloatField(required=True)
    width = serializers.FloatField(required=True)
    height = serializers.FloatField(required=True)
    weight = serializers.FloatField(required=True)
    category = serializers.ChoiceField(choices=BoxCategory.choices, required=True)
    quantity = serializers.IntegerField(min_value=1, default=1)


class RecommendationRequestSerializer(serializers.Serializer):
    items = RecommendationItemSerializer(many=True, required=True)
