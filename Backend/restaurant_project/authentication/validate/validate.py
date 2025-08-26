import re
from rest_framework import serializers


class ValidateData:

    @staticmethod
    def validate_password(value):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
                "Passwords must have at least one special character"
            )
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Passwords must have at least one number")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "Passwords must have at least one upper character"
            )
        if any(char.isspace() for char in value):
            raise serializers.ValidationError("Passwords cannot have spaces")
        if not value:
            raise serializers.ValidationError("Passwords cannot be empty")
        return value

    @staticmethod
    def validate_email(value):
        if not (re.search(r"[^@]*@[^@]*$", value)):
            raise serializers.ValidationError(
                "Invalid email format. Please include the @ symbol."
            )
        if value == "":
            raise serializers.ValidationError("Email cannot empty")
        return value
