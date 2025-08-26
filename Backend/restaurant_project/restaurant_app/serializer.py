from rest_framework import serializers
from restaurant_app.models import *
from rest_framework.exceptions import AuthenticationFailed
import re
from django.conf import settings


class EmployeeSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(queryset=ManagerAccount.objects.all())

    class Meta:
        model = EmployeeInformation
        fields = "__all__"

    def validate_email(self, value):
        if not (re.search(r"[^@]*@[^@]*$", value)):
            raise serializers.ValidationError(
                "Invalid email format. Please include the @ symbol."
            )
        if value == "":
            raise serializers.ValidationError("Email cannot empty")
        return value


class CustomerBookingInfoSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=CustomerAccount.objects.all()
    )

    class Meta:
        model = CustomerBookingInformation
        fields = "__all__"
        extra_kwargs = {
            "note": {"required": False},
        }

    def create(self, validated_data):
        customer_id = validated_data.pop("customer")
        customer = CustomerAccount.objects.get(pk=customer_id)
        booking = CustomerBookingInformation.objects.create(
            customer=customer, **validated_data
        )
        return booking


class FeedbackFromcustomerSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=CustomerAccount.objects.all()
    )

    class Meta:
        model = FeedbackFromCustomer
        fields = ("feedback", "customer")
        read_only_fields = ["customer"]


class MenuItemSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(queryset=ManagerAccount.objects.all())

    class Meta:
        model = MenuItems
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("menu_item", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    customer = serializers.PrimaryKeyRelatedField(
        queryset=CustomerAccount.objects.all()
    )

    class Meta:
        model = Order
        fields = ("customer", "total_price", "status", "items")

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        total_price = 0

        for item_data in items_data:
            menu_item = item_data["menu_item"]
            quantity = item_data["quantity"]
            price = menu_item.price * quantity

            OrderItem.objects.create(
                order=order, menu_item=menu_item, quantity=quantity, price=price
            )
            total_price += price
            order.total_price = total_price
        order.save()
        return order


class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()

    class Meta:
        model = CartItem
        fields = ("menu_item", "quantity")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    customer = serializers.PrimaryKeyRelatedField(
        queryset=CustomerAccount.objects.all()
    )

    class Meta:
        model = Cart
        fields = ("customer", "items")


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Payment
        fields = "__all__"
