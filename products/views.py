from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer
import random

class ProductPublicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related('product_images').order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        pagination_param = request.query_params.get('pagination', '').lower()
        queryset = self.get_queryset()

        if pagination_param in ['true', '1', 'yes']:
            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_qs = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(paginated_qs, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        random.shuffle(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductAdminViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all().order_by('-uploaded_at')
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAdminUser]
