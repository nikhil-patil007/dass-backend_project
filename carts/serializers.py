from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "product", "product_id", "quantity", "added_at")
        read_only_fields = ("id", "product", "added_at")

    def create(self, validated_data):
        cart = self.context['cart']
        product_id = validated_data.pop('product_id')
        quantity = validated_data.get('quantity', 1)
        item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id, defaults={'quantity': quantity})
        if not created:
            item.quantity += quantity
            item.save()
        return item


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ("id", "user", "items")
        read_only_fields = ("id", "user")
