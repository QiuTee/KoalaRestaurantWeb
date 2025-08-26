from django.apps import AppConfig
import sys

class RestaurantAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "restaurant_app"

    def ready(self):
        if 'runserver' in sys.argv:
            import restaurant_app.order.order_history
            from django.contrib.auth.models import Group
            GROUPS = ['admin', 'anonymous', 'manager', 'customer']
            
            for group_name in GROUPS:
                group, created = Group.objects.get_or_create(name=group_name)
                if created:
                    print(f"Group '{group_name}' được tạo thành công.")
                else:
                    print(f"Group '{group_name}' đã tồn tại.")

    
        
