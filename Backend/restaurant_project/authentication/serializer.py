from rest_framework import serializers
from .utils import *
from .factories.account_factories import ManagerAccountFactory, CustomerAccountFactory
from .validate.validate import ValidateData


class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length=6)

    def validate_access_token(self, access_token):
        google_user_data = Google.validate(access_token)

        try:
            userid = google_user_data["sub"]
        except:
            raise serializers.ValidationError("This token is invalid or has expired")
        if google_user_data["aud"] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed(detail="Could not verify user")
        email = google_user_data["email"]
        first_name = google_user_data["given_name"]
        last_name = google_user_data["family_name"]
        provider = "google"
        return register_social_user(provider, email, first_name, last_name)


class BaseAccountSerializer(serializers.ModelSerializer):
    factory_class = None

    def create(self, validated_data):
        if not self.factory_class():
            raise NotImplemented("Factory class must be define in the serializer")
        factory = self.factory_class()
        return factory.create_user(validated_data)


class MangerAccountSerializer(BaseAccountSerializer):
    factory_class = ManagerAccountFactory

    class Meta:
        model = ManagerAccount
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "address",
            "phone_number",
            "manager_fullname",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        ValidateData.validate_email(attrs.get("email"))
        ValidateData.validate_password(attrs.get("password"))
        return attrs


class CustomerAccountSerializer(BaseAccountSerializer):
    retype_password = serializers.CharField(write_only=True, required=True)
    factory_class = CustomerAccountFactory

    class Meta:
        model = CustomerAccount
        fields = (
            "email",
            "password",
            "last_name",
            "first_name",
            "address",
            "retype_password",
            "phone_number",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        ValidateData.validate_email(attrs.get("email"))
        ValidateData.validate_password(attrs.get("password"))
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True, required=True)
