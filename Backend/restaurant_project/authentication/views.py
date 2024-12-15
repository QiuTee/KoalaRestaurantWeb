from response.responses import Responses
from rest_framework import generics
from authentication.serializer import GoogleSignInSerializer , MangerAccountSerializer , CustomerAccountSerializer, LoginSerializer
from rest_framework import viewsets
from authentication.models import ManagerAccount , CustomerAccount
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from abc import abstractmethod


class GoogleSignInView(generics.GenericAPIView):
    serializer_class = GoogleSignInSerializer
    
    def post(self , request):
      
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['access_token'])
        return Responses.response_api("Successfull","200 OK", data=data )
    
    


class BaseAuthenticationsViewset(viewsets.ModelViewSet):
    @abstractmethod
    def get_serializer_class(self):
        pass 
    
    def get_serializer_class_with_action(self):
        if self.action == 'login':
            return LoginSerializer
        return self.get_serializer_class()
    
    @action(detail=False , methods=['POST'])
    def register(self , request): 
        data = request.data 
        if data.get('password') != data.get('retype_password'):
            return Responses.response_api("Password and Retype Password is not match","400")
        
        serializer = self.get_serializer(data = data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save() 
                return Responses.response_api('Register successfully','200')
        except Exception as e : 
            return Responses.response_api('Register unsuccesfully','400', error=str(e))
        
    @action(detail=False, methods=['POST'])
    def login(self, request):
        data = request.data 
        print(data)
        serializer = self.get_serializer_class_with_action()(data = data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email = email ,password =  password)
            user_tokens = user.tokens()

            data = {
                    'access' : str(user_tokens.get('access')),
                    'refresh':str(user_tokens.get('refresh'))
                }
            return Responses.response_api('Login successfully','200', data=data)
        
class ManagerAuthentications(BaseAuthenticationsViewset):
    queryset = ManagerAccount.objects.all() 
    
    def get_serializer_class(self):
        return MangerAccountSerializer
    
class CustomerAuthentications(BaseAuthenticationsViewset):
    queryset = CustomerAccount.objects.all()
    
    def get_serializer_class(self):
        return CustomerAccountSerializer