from django.db import models
from authentication.manager import *
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from cloudinary.models import CloudinaryField
from authentication.models import *


class EmployeeInformation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manager = models.ForeignKey(
        ManagerAccount, on_delete=models.CASCADE, related_name="employee"
    )
    image = CloudinaryField("image")
    employee_name = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, unique=True)
    phone = models.IntegerField(
        validators=[MinValueValidator(100000000), MaxValueValidator(9999999999)]
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(max_length=20, null=False)


class CustomerBookingInformation(models.Model):

    customer = models.ForeignKey(
        CustomerAccount, on_delete=models.CASCADE, related_name="Bookings"
    )
    email = models.CharField(max_length=50, null=False)
    customer_name = models.CharField(max_length=255, null=False)
    phone_number = models.IntegerField(
        validators=[MinValueValidator(100000000), MaxValueValidator(9999999999)]
    )
    number_of_guest = models.IntegerField()
    date = models.DateField(max_length=20, null=False)
    time = models.TimeField(max_length=20, null=False)
    note = models.CharField(max_length=255, null=True, blank=True)


class FeedbackFromCustomer(models.Model):
    customer = models.ForeignKey(
        CustomerAccount, on_delete=models.CASCADE, related_name="Bookings"
    )
    feedback = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(BaseUser, on_delete=models.CASCADE)


class MenuItems(models.Model):
    manager = models.ForeignKey(
        ManagerAccount, on_delete=models.CASCADE, related_name="item"
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = CloudinaryField("image")
    food_name = models.CharField(max_length=50, null=False, unique=True)
    category = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    stock = models.IntegerField()
    status = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=255, null=False)


class Order(models.Model):
    customer = models.ForeignKey(
        CustomerAccount, on_delete=models.CASCADE, related_name="orders"
    )
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Pending",
    )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(
        MenuItems, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=3)


class OrderHistory(models.Model):
    customer = models.ForeignKey(
        CustomerAccount, on_delete=models.CASCADE, related_name="order_history"
    )
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.CharField(max_length=40)
    items = models.JSONField()


class Cart(models.Model):
    customer = models.ForeignKey(
        CustomerAccount, on_delete=models.CASCADE, related_name="cart"
    )


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(
        MenuItems, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=3)


class Payment(models.Model):
    PAYMENT_METHOD = (("cash", "Cash"), ("bank", "Bank Transfer"))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")
