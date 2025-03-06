from django.utils import timezone
from rest_framework import status, viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import TaskSerializer
from .models import Task

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["priority", "due_date", "created_at"]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user, is_deleted=False)

        status_param = self.request.query_params.get("status")
        priority_param = self.request.query_params.get("priority")
        due_date_param = self.request.query_params.get("due_date")

        if status_param:
            queryset = queryset.filter(status=status_param)
        if priority_param:
            queryset = queryset.filter(priority=priority_param)
        if due_date_param:
            queryset = queryset.filter(due_date=due_date_param)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_deleted = True
        task.deleted_at = timezone.now()
        task.save()
        return Response({"message": "Task soft deleted successfully!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk, user=request.user, is_deleted=True)
            task.is_deleted = False
            task.deleted_at = None
            task.save()
            return Response({"message": "Task restored successfully!"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)