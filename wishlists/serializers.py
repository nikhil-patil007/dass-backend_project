from rest_framework import serializers
from .models import Wishlist, WishlistItem
from products.serializers import ProductSerializer


class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = WishlistItem
        fields = ("id", "product", "product_id", "added_at")
        read_only_fields = ("id", "product", "added_at")

    def create(self, validated_data):
        wishlist = self.context['wishlist']
        product_id = validated_data.pop('product_id')
        item, _ = WishlistItem.objects.get_or_create(wishlist=wishlist, product_id=product_id)
        return item


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, required=False)

    class Meta:
        model = Wishlist
        fields = ("id", "name", "user", "items")
        read_only_fields = ("id", "user")

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        wishlist = Wishlist.objects.create(**validated_data)
        for item in items_data:
            product_id = item.get('product_id')
            if product_id:
                WishlistItem.objects.get_or_create(wishlist=wishlist, product_id=product_id)
        return wishlist
