from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Box, Product
from core.serializers import BoxSerializer, ProductSerializer, RecommendationRequestSerializer
from core.services.ai_classifier import classify_product_category
from core.services.recommendation import recommend_box_for_items


class ProductListCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if "category" not in data or data["category"] in (None, ""):
            data["category"] = classify_product_category(data.get("title", ""), data.get("description", ""))

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def patch(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoxListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        boxes = Box.objects.all().order_by("cost")
        serializer = BoxSerializer(boxes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = BoxSerializer(data=request.data)
        if serializer.is_valid():
            box = serializer.save()
            return Response(BoxSerializer(box).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendBoxView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RecommendationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            recommendation = recommend_box_for_items(serializer.validated_data["items"])
            return Response(recommendation)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
