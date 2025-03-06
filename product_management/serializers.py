from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    """ Serializer for Category with nested subcategories """
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent_category', 'subcategories', 'is_active', 'created_at', 'updated_at']

    def get_subcategories(self, obj):
        """ Retrieve nested subcategories for a category """
        subcategories = Category.objects.filter(parent_category=obj, is_deleted=False)
        return CategorySerializer(subcategories, many=True).data

class ProductSerializer(serializers.ModelSerializer):
    """ Serializer for Product """
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'category', 'category_name', 'name', 'price', 'stock', 'description', 'is_active', 'created_at', 'updated_at']