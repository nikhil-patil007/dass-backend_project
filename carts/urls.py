from django.urls import path
from .views import CartView, AddCartItemView, RemoveCartItemView

urlpatterns = [
    path('', CartView.as_view(), name='cart-detail'),
    path('items/add/', AddCartItemView.as_view(), name='cart-item-add'),
    path('items/<uuid:item_id>/remove/', RemoveCartItemView.as_view(), name='cart-item-remove'),
]
