from abc import ABC, abstractmethod
from ..models import ManagerAccount, CustomerAccount
from django.contrib.auth.models import Group


class AccountFactory(ABC):
    @abstractmethod
    def create_user(self, validated_data):
        pass


class ManagerAccountFactory(AccountFactory):
    def create_user(self, validated_data):
        password = validated_data.get("password")
        email = validated_data.get("email")
        last_name = validated_data.get("last_name")
        first_name = validated_data.get("first_name")
        address = validated_data.get("address")
        phone_number = validated_data.get("phone_number")
        manager_fullname = validated_data.get("manager_fullname")
        manage_group, create_group = Group.objects.get_or_create(name="manager")

        user = ManagerAccount.objects.create_user(
            manager_fullname=manager_fullname,
            password=password,
            email=email,
            last_name=last_name,
            first_name=first_name,
            address=address,
            phone_number=phone_number,
            is_active=True,
            group=manage_group,
            is_manager=True,
        )
        return user


class CustomerAccountFactory(AccountFactory):
    def create_user(self, validated_data):
        password = validated_data.get("password")
        email = validated_data.get("email")
        last_name = validated_data.get("last_name")
        first_name = validated_data.get("first_name")
        address = validated_data.get("address")
        phone_number = validated_data.get("phone_number")
        customer_name = f"{last_name} {first_name}"
        customer_group = Group.objects.get(name="customer")
        # Tạo đối tượng `CustomerAccount` với `customer_name` đã được tính toán
        user = CustomerAccount.objects.create_user(
            customer_name=customer_name,
            password=password,
            email=email,
            last_name=last_name,
            first_name=first_name,
            address=address,
            is_active=True,
            phone_number=phone_number,
            group=customer_group,
        )
        return user
