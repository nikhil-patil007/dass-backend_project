from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404


class OrderListCreateView(generics.ListCreateAPIView):
    """
    List all orders for the current user or create a new order.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.context['request'] = self.request
        serializer.save()


class OrderDetailView(generics.RetrieveAPIView):
    """
    Retrieve the details of a specific order for the current user.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Order, id=self.kwargs.get('pk'), user=self.request.user)
