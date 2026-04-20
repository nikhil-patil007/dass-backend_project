from rest_framework import permissions, generics
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    """Public product list view. Supports optional pagination via ?pagination=true
    and optional random ordering via ?random=true.
    """
    queryset = Product.objects.select_related('category').prefetch_related('product_images').order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        pagination_param = request.query_params.get('pagination', '').lower()
        random_param = request.query_params.get('random', '').lower()

        queryset = self.get_queryset()

        if random_param in ['true', '1', 'yes']:
            queryset = queryset.order_by('?')

        if pagination_param in ['true', '1', 'yes']:
            return super().list(request, *args, **kwargs)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related('category').prefetch_related('product_images')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
