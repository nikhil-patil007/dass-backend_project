from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_id", "quantity", "unit_price")
        read_only_fields = ("id", "product", "unit_price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "user", "total_amount", "status", "items", "created_at")
        read_only_fields = ("id", "user", "total_amount", "created_at")

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user)
        total = 0
        for item in items_data:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            product = ProductSerializer().Meta.model.objects.get(id=product_id)
            unit_price = product.price
            OrderItem.objects.create(order=order, product=product, quantity=quantity, unit_price=unit_price)
            total += unit_price * quantity
        order.total_amount = total
        order.save()
        return order
