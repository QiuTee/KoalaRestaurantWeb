from ..models import *
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender = Order)
def add_order_into_orderhistory( sender , instance , **kwargs):
    if instance.status == "complete": 
        order_item = OrderItem.objects.filter(order = instance).first() 
        item_data = [
            { 
            "menu_item": item.menu_item,
            "quantity" : item.quantity,
            "price" : item.price      
            }
            for item in order_item 
        ]
        
        OrderHistory.objects.create(
            customer = instance.customer, 
            total_price = instance.total_price, 
            status = instance.status, 
            items = item_data
        )
        order_item.delete() 
        instance.delete()