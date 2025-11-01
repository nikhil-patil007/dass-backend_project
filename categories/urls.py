from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryPublicViewSet, CategoryAdminViewSet

router = DefaultRouter()
router.register(r'', CategoryPublicViewSet, basename='public-category')
router.register(r'admin/categories', CategoryAdminViewSet, basename='admin-category')

urlpatterns = [
    path('', include(router.urls)),
]
