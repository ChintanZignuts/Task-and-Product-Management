from django.utils import timezone
from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser
from rest_framework.views import APIView
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_deleted=False,parent_category__isnull=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

class SoftDeleteCategoryView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.is_deleted = True
            category.deleted_at = timezone.now()
            category.save()
            return Response({"message": "Category soft deleted"}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

class RestoreCategoryView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def post(self, request, pk):
        try:
            category = Category.objects.get(pk=pk, is_deleted=True)
            category.is_deleted = False
            category.deleted_at = None
            category.save()
            return Response({"message": "Category restored"}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at", "name"]

    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)

        category = self.request.query_params.get("category")
        is_active = self.request.query_params.get("is_active")

        if category:
            queryset = queryset.filter(category=category)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() in ["true", "1"])

        return queryset

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

class SoftDeleteProductView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, is_deleted=False)
            product.is_deleted = True
            product.deleted_at = timezone.now()
            product.save()
            return Response({"message": "Product soft deleted"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

class RestoreProductView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, is_deleted=True)
            product.is_deleted = False
            product.deleted_at = None
            product.save()
            return Response({"message": "Product restored"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)