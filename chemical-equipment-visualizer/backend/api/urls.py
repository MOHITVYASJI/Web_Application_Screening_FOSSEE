"""
URL configuration for API endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    register_user,
    login_user,
    current_user,
    DatasetViewSet
)

# Create router for viewsets
router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')

app_name = 'api'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/me/', current_user, name='current-user'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Dataset endpoints (handled by router)
    # GET    /api/datasets/                  - List datasets
    # POST   /api/datasets/upload/           - Upload new dataset
    # GET    /api/datasets/{id}/             - Get dataset details
    # DELETE /api/datasets/{id}/             - Delete dataset
    # GET    /api/datasets/{id}/statistics/  - Get statistics
    # GET    /api/datasets/{id}/download_pdf/ - Download PDF report
    path('', include(router.urls)),
]