from django.urls import path
from .views import (
    WishlistListCreateView,
    WishlistDetailView,
    AddWishlistItemView,
    RemoveWishlistItemView,
)

urlpatterns = [
    path('', WishlistListCreateView.as_view(), name='wishlist-list'),
    path('<uuid:pk>/', WishlistDetailView.as_view(), name='wishlist-detail'),
    path('<uuid:pk>/items/add/', AddWishlistItemView.as_view(), name='wishlist-item-add'),
    path('<uuid:pk>/items/<uuid:item_id>/remove/', RemoveWishlistItemView.as_view(), name='wishlist-item-remove'),
]
