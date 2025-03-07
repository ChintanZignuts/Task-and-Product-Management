from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from tasks.models import Task

User = get_user_model()

class TaskManagementTests(APITestCase):
    def setUp(self):
        """Create a user and a sample task."""
        self.user = User.objects.create_user(username='user', email='user@example.com', password='userpass')
        self.task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="This is a test task",
            due_date="2025-12-31",
            priority="high",
            status="pending",
        )
        self.task_url = f"/api/tasks/{self.task.id}/"

    def authenticate(self):
        self.client.force_authenticate(user=self.user)
    
    def test_user_can_create_task(self):
        self.authenticate()
        response = self.client.post("/api/tasks/", {
            "title": "New Task",
            "description": "Task description",
            "due_date": "2025-12-31",
            "priority": "medium",
            "status": "pending"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_can_get_task_list(self):
        self.authenticate()
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_can_retrieve_task(self):
        self.authenticate()
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_can_update_task(self):
        self.authenticate()
        response = self.client.put(self.task_url, {
            "title": "Updated Task",
            "description": "Updated description",
            "due_date": "2025-12-31",
            "priority": "low",
            "status": "in_progress"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_can_delete_task(self):
        self.authenticate()
        response = self.client.delete(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_user_cannot_create_task(self):
        response = self.client.post("/api/tasks/", {
            "title": "Unauthorized Task",
            "description": "Should fail",
            "due_date": "2025-12-31",
            "priority": "high",
            "status": "pending"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthenticated_user_cannot_delete_task(self):
        response = self.client.delete(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
