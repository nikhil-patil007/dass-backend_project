from rest_framework import permissions, generics
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    """Public category list view. Supports optional pagination via ?pagination=true
    and optional random ordering via ?random=true.
    """
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
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


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# Admin viewset removed — only public list/detail APIs remain
