from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from product_management.models import Product, Category

User = get_user_model()

class ProductManagementTests(APITestCase):
    def setUp(self):
        """Create an admin user, normal user, and a category for products."""
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass',role='admin')
        self.normal_user = User.objects.create_user(username='user', email='user@example.com', password='userpass')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(name='Laptop', category=self.category, price=1200.00)
        self.product_url = f"/api/products/{self.product.id}/"

    def authenticate_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
    
    def authenticate_as_user(self):
        self.client.force_authenticate(user=self.normal_user)
    
    def test_admin_can_create_product(self):
        self.authenticate_as_admin()
        response = self.client.post("/api/products/", {
            "name": "Smartphone",
            "category": self.category.id,
            "price": 800.00
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_cannot_create_product(self):
        self.authenticate_as_user()
        response = self.client.post("/api/products/", {
            "name": "Smartphone",
            "category": self.category.id,
            "price": 800.00
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_can_get_product_list(self):
        self.authenticate_as_admin()
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_admin_can_retrieve_product(self):
        self.authenticate_as_admin()
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_admin_can_update_product(self):
        self.authenticate_as_admin()
        response = self.client.put(self.product_url, {
            "name": "Gaming Laptop",
            "category": self.category.id,
            "price": 1500.00
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_cannot_update_product(self):
        self.authenticate_as_user()
        response = self.client.put(self.product_url, {
            "name": "Gaming Laptop",
            "category": self.category.id,
            "price": 1500.00
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_can_soft_delete_product(self):
        self.authenticate_as_admin()
        delete_url = f"{self.product_url}delete/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_admin_can_restore_product(self):
        self.authenticate_as_admin()
        delete_url = f"{self.product_url}delete/"
        restore_url = f"{self.product_url}restore/"
        self.client.delete(delete_url)
        response = self.client.post(restore_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_cannot_delete_product(self):
        self.authenticate_as_user()
        delete_url = f"{self.product_url}delete/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
