from response.responses import Responses
from rest_framework import generics
from authentication.serializer import (
    GoogleSignInSerializer,
    MangerAccountSerializer,
    CustomerAccountSerializer,
    LoginSerializer,
)
from rest_framework import viewsets
from authentication.models import ManagerAccount, CustomerAccount
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from abc import abstractmethod
from .throttle import UserLoginRateThrottle
from rest_framework.exceptions import Throttled
from .permission import IsManagerUser


class GoogleSignInView(generics.GenericAPIView):
    serializer_class = GoogleSignInSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["access_token"]
        return Responses.response_api("Successfull", "200 OK", data=data)


class BaseAuthenticationsViewset(viewsets.ModelViewSet):
    @abstractmethod
    def get_serializer_class(self):
        pass

    def get_serializer_class_with_action(self):
        if self.action == "login":
            return LoginSerializer
        return self.get_serializer_class()

    # def get_permissions(self):
    #     if self.action == "login" and isinstance(self, ManagerAuthentications):
    #         return [IsManagerUser()]
    #     return super().get_permissions()

    @action(detail=False, methods=["POST"])
    def register(self, request):
        data = request.data
        if data.get("password") != data.get("retype_password"):
            return Responses.response_api(
                "Password and Retype Password is not match", "400"
            )

        serializer = self.get_serializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Responses.response_api("Register successfully", "200")
        except Exception as e:
            return Responses.response_api("Register unsuccesfully", "400", error=str(e))

    @action(detail=False, methods=["POST"])
    def login(self, request):
        data = request.data
        print(data)
        serializer = self.get_serializer_class_with_action()(data=data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            try:
                user = authenticate(email=email, password=password)
                print(user.is_manager)

                if not user:
                    raise Throttled(
                        detail="Too many login attempts.Please complete the reCaptcha"
                    )
                user_tokens = user.tokens()
                if isinstance(self, ManagerAuthentications) and not user.is_manager:
                    return Responses.response_api(
                        "You are not allow to access this page", "400"
                    )
                data = {
                    "access": str(user_tokens.get("access")),
                    "refresh": str(user_tokens.get("refresh")),
                }
                print("Successfully")
                return Responses.response_api("Login successfully", "200", data=data)
            except Exception as e:
                print(str(e))
                return Responses.response_api("Error", "400", error=str(e))


class ManagerAuthentications(BaseAuthenticationsViewset):
    queryset = ManagerAccount.objects.all()
    throttle_classes = [UserLoginRateThrottle]

    def get_serializer_class(self):
        return MangerAccountSerializer


class CustomerAuthentications(BaseAuthenticationsViewset):
    queryset = CustomerAccount.objects.all()
    throttle_classes = [UserLoginRateThrottle]

    def get_serializer_class(self):
        return CustomerAccountSerializer
