from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductPublicViewSet, ProductAdminViewSet, ProductImageViewSet

router = DefaultRouter()
router.register(r'', ProductPublicViewSet, basename='public-product')
router.register(r'admin/products', ProductAdminViewSet, basename='admin-product')
router.register(r'admin/product-images', ProductImageViewSet, basename='product-image')

urlpatterns = [
    path('', include(router.urls)),
]
