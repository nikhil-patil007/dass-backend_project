from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Category
from .serializers import CategorySerializer
import random

class CategoryPublicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('?')
    serializer_class = CategorySerializer
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

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class CategoryAdminViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
