from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/', include('product_management.urls')),
    path('api/tasks/', include('tasks.urls')),
]
