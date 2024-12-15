from rest_framework import serializers
from .utils import *
import re
class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length = 6)
    
    def validate_access_token(self, access_token):
        google_user_data = Google.validate(access_token)
        
        try: 
            userid = google_user_data["sub"]
        except:
            raise serializers.ValidationError("This token is invalid or has expired")
        if google_user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed(detail="Could not verify user")
        email = google_user_data['email']
        first_name = google_user_data['given_name']
        last_name = google_user_data['family_name']
        provider = "google"
        return register_social_user(provider,email,first_name,last_name)
    
    
    
    
    
class MangerAccountSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = ManagerAccount
        fields = ('email','password','first_name','last_name','address','phone_number','manager_fullname')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def validate_password(self, value):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Passwords must have at least one special character")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Passwords must have at least one number")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Passwords must have at least one upper character")
        if any(char.isspace() for char in value):
            raise serializers.ValidationError("Passwords cannot have spaces" )
        if not value:
            raise serializers.ValidationError("Passwords cannot be empty") 
        return value

    def validate_email(self, value):
        if not (re.search(r'[^@]*@[^@]*$' , value) ):
            raise serializers.ValidationError("Invalid email format. Please include the @ symbol.")
        if value == "": 
            raise serializers.ValidationError("Email cannot empty")
        return value
       
    def create(self, validated_data):
        password = validated_data.get('password')
        email = validated_data.get('email')
        last_name = validated_data.get('last_name')
        first_name = validated_data.get('first_name')
        address = validated_data.get('address')
        phone_number = validated_data.get('phone_number')
        manager_fullname = validated_data.get('manager_fullname')
        manage_group , create_group = Group.objects.get_or_create(name = 'manager')

        user = ManagerAccount.objects.create_user(
            manager_fullname=manager_fullname,
            password=password,
            email=email,
            last_name=last_name,
            first_name=first_name,
            address=address,
            phone_number = phone_number, 
            is_active=True , 
            group = manage_group
            )
        return user
    
class CustomerAccountSerializer(serializers.ModelSerializer):
    retype_password = serializers.CharField(write_only = True , required = True)

    class Meta:
        model = CustomerAccount
        fields = ('email', 'password', 'last_name', 'first_name','address','retype_password','phone_number')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def validate_password(self, value):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Passwords must have at least one special character")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Passwords must have at least one number")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Passwords must have at least one upper character")
        if any(char.isspace() for char in value):
            raise serializers.ValidationError("Passwords cannot have spaces" )
        if not value:
            raise serializers.ValidationError("Passwords cannot be empty") 
        return value

    def validate_email(self, value):
        if not (re.search(r'[^@]*@[^@]*$' , value) ):
            raise serializers.ValidationError("Invalid email format. Please include the @ symbol.")
        if value == "": 
            raise serializers.ValidationError("Email cannot empty")
        return value
    
     
    def create(self, validated_data):
        password = validated_data.get('password')
        email = validated_data.get('email')
        last_name = validated_data.get('last_name')
        first_name = validated_data.get('first_name')
        address = validated_data.get('address')
        phone_number = validated_data.get('phone_number')
        customer_name = f"{last_name} {first_name}"
        customer_group = Group.objects.get(name = 'customer')
        # Tạo đối tượng `CustomerAccount` với `customer_name` đã được tính toán
        user = CustomerAccount.objects.create_user(
            customer_name=customer_name,
            password=password,
            email=email,
            last_name=last_name,
            first_name=first_name,
            address=address,
            is_active=True,
            phone_number = phone_number,
            group = customer_group
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length= 50)
    password = serializers.CharField(write_only = True , required = True)