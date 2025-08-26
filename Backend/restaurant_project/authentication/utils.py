from google.auth.transport import requests
from google.oauth2 import id_token
from .models import *
from django.contrib.auth import authenticate
from django.conf import settings 
from rest_framework.exceptions import AuthenticationFailed


class Google():
    @staticmethod
    def validate(access_token):
        try:
            #Verifies an ID Token issued by Google's OAuth 2.0 authorization server.
            id_inf = id_token.verify_oauth2_token(access_token , requests.Request())
            if "accounts.google.com" in id_inf['iss']:
                return id_inf
        except Exception as e : 
            return "Token is invalid or has expired"
        
def login_user(email, password):
    print(email)
    print(password)
    user = authenticate(email = email , password = password)
    print(user)
    user_tokens = user.tokens()
    return {
        'email':user.email,
        'full_name':user.get_full_name,
        'access_token' : str(user_tokens.get('access')),
        'refresh_token':str(user_tokens.get('refresh'))
    }


        
def register_social_user(provider, email, first_name, last_name): 
    user = BaseUser.objects.filter(email = email )
    if user.exists():
        if provider == user[0].auth_provider:
            login_user(email, settings.SOCIAL_AUTH_PASSWORD)
        else: 
            raise AuthenticationFailed(
                detail=f"Please continue login with {user[0].auth_provider}"
            )
            
    else:
        manage_group , create_group = Group.objects.get_or_create(name = 'customer')
        new_user={
            'email':email,
            'first_name':first_name,
            'last_name':last_name,
            'password':settings.SOCIAL_AUTH_PASSWORD,
            "group_id": manage_group.id
        }
        register_user = BaseUser.objects.create(**new_user)
        register_user.auth_provider = provider 
        register_user.is_verified = True
        register_user.save()
        
        login_user(email, settings.SOCIAL_AUTH_PASSWORD)