from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from .manager import UserManager, CustomerManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import MinValueValidator, MaxValueValidator


AUTH_PROVIDERS = {
    "email": "email",
    "google": "google",
    "github": "github",
    "facebook": "facebook",
}


class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=255, verbose_name=("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=("Last Name"))
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)
    is_manager = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=50, default=AUTH_PROVIDERS.get("email"))
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    @property
    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        refresh["email"] = self.email
        refresh["role"] = self.group.name
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


# ManagerAccount model
class ManagerAccount(BaseUser):
    manager_fullname = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    phone_number = models.IntegerField(
        validators=[MinValueValidator(100000000), MaxValueValidator(9999999999)]
    )
    start_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    def __str__(self):
        return f"Manager: {self.email}"


class CustomerAccount(BaseUser):
    phone_number = models.IntegerField(
        validators=[MinValueValidator(10000000), MaxValueValidator(99999999999)]
    )
    customer_name = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    join_date = models.DateField(auto_now_add=True)
    USERNAME_FIELD = "email"

    objects = CustomerManager()

    def __str__(self):
        return f"Customer: {self.email}"
