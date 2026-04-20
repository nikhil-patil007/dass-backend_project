from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404
from django.conf import settings


class CartView(generics.RetrieveAPIView):
    """
    Retrieve the current user's shopping cart.
    Creates a new cart if one doesn't exist.
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddCartItemView(generics.CreateAPIView):
    """
    Add an item to the current user's shopping cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.context['cart'] = cart
        serializer.save()


class RemoveCartItemView(generics.DestroyAPIView):
    """
    Remove an item from the current user's shopping cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'item_id'

    def get_object(self):
        cart = get_object_or_404(Cart, user=self.request.user)
        return get_object_or_404(CartItem, cart=cart, id=self.kwargs.get(self.lookup_url_kwarg))

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
