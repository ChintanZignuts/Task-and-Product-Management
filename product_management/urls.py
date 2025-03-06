from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView, SoftDeleteCategoryView, RestoreCategoryView,
    ProductListCreateView, ProductDetailView, SoftDeleteProductView, RestoreProductView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/delete/', SoftDeleteCategoryView.as_view(), name='category-soft-delete'),
    path('categories/<int:pk>/restore/', RestoreCategoryView.as_view(), name='category-restore'),
    
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/delete/', SoftDeleteProductView.as_view(), name='product-soft-delete'),
    path('products/<int:pk>/restore/', RestoreProductView.as_view(), name='product-restore'),
]