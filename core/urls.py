from django.urls import path

from core.views import BoxListCreateView, ProductDetailView, ProductListCreateView, RecommendBoxView

urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="products-list-create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="products-detail"),
    path("boxes/", BoxListCreateView.as_view(), name="boxes-list-create"),
    path("recommend-box/", RecommendBoxView.as_view(), name="recommend-box"),
]
