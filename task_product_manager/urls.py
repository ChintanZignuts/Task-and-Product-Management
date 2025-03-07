from django.contrib import admin
from django.urls import path,include
from authentication.views import health_check
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"), 
    path("api/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"), 
    path('',health_check,name='health_check'),
    path('api/auth/', include('authentication.urls')),
    path('api/', include('product_management.urls')),
    path('api/tasks/', include('tasks.urls')),
]
