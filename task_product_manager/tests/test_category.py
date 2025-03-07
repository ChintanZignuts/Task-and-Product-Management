from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from product_management.models import Category

User = get_user_model()
class CategoryManagementTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            email="admin@example.com",
            password="AdminPassword123",
            role='admin'
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="TestPassword123"
        )
        self.category = Category.objects.create(name="Electronics")
        self.category_url = "/api/categories/"
        self.category_detail_url = f"/api/categories/{self.category.id}/"
        
    def authenticate_as_admin(self):
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def authenticate_as_user(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_admin_can_create_category(self):
        self.authenticate_as_admin()
        data = {"name": "Books"}
        response = self.client.post(self.category_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Books")

    def test_user_cannot_create_category(self):
        self.authenticate_as_user()
        data = {"name": "Books"}
        response = self.client.post(self.category_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_categories(self):
        self.authenticate_as_admin()
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_update_category(self):
        self.authenticate_as_admin()
        data = {"name": "Updated Electronics"}
        response = self.client.put(self.category_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Electronics")

    def test_admin_can_soft_delete_category(self):
        self.authenticate_as_admin()
        delete_url = f"/api/categories/{self.category.id}/delete/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_restore_category(self):
        self.authenticate_as_admin()

        delete_url = f"/api/categories/{self.category.id}/delete/"
        self.client.delete(delete_url)

        self.category.refresh_from_db()

        restore_url = f"/api/categories/{self.category.id}/restore/"
        response = self.client.post(restore_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
