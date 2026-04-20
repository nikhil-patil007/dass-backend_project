from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Wishlist, WishlistItem
from .serializers import WishlistSerializer, WishlistItemSerializer
from django.shortcuts import get_object_or_404


class WishlistListCreateView(generics.ListCreateAPIView):
	"""
	List all wishlists for the current user or create a new wishlist.
	"""
	serializer_class = WishlistSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Wishlist.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class WishlistDetailView(generics.RetrieveDestroyAPIView):
	"""
	Retrieve or delete a specific wishlist for the current user.
	"""
	serializer_class = WishlistSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		return get_object_or_404(Wishlist, id=self.kwargs.get('pk'), user=self.request.user)


class AddWishlistItemView(generics.CreateAPIView):
	"""
	Add an item to a specific wishlist.
	"""
	serializer_class = WishlistItemSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		wishlist = get_object_or_404(Wishlist, id=self.kwargs.get('pk'), user=self.request.user)
		serializer.context['wishlist'] = wishlist
		serializer.save()


class RemoveWishlistItemView(generics.DestroyAPIView):
	"""
	Remove an item from a specific wishlist.
	"""
	serializer_class = WishlistItemSerializer
	permission_classes = [permissions.IsAuthenticated]
	lookup_url_kwarg = 'item_id'

	def get_object(self):
		wishlist = get_object_or_404(Wishlist, id=self.kwargs.get('pk'), user=self.request.user)
		return get_object_or_404(WishlistItem, wishlist=wishlist, id=self.kwargs.get(self.lookup_url_kwarg))

	def delete(self, request, *args, **kwargs):
		obj = self.get_object()
		obj.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
