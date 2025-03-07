from django.contrib import admin
from django.urls import path,include
from authentication.views import health_check
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',health_check,name='health_check'),
    path('api/auth/', include('authentication.urls')),
    path('api/', include('product_management.urls')),
    path('api/tasks/', include('tasks.urls')),
]
