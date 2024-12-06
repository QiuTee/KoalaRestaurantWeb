
from rest_framework import  viewsets
from .response.responses import Responses 
from restaurant_app.serializer import *
from restaurant_app.models import *
from rest_framework.decorators import action 
from rest_framework import generics 
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from .permission import *
# Create your views here.
# class RegisterAndLoginForCustomer(viewsets.ModelViewSet) : 
#     queryset = User.objects.all() 
#     serializer_class = UserInfoSerializer
    
#     @action(detail = False , methods = ['POST'])
#     def customer_register(self, request) :
#         data = JSONParser().parse(request)
#         password = data.get('password')
#         retypePassword = data.get('retypePassword')

#         # Check the match of the password and re-entered password
#         if not password == retypePassword :
#             return Responses.response_api('Password and Retype Password is not match','401 Unauthorized')
#         serializers = UserInfoSerializer( data = data )
#         # print(data)
#         try :
#             # Check the validity of input data from serializers
#             if serializers.is_valid(raise_exception= True) :
#                 user = serializers.save()
#                 data = {
#                         'id': user.id,
#                         'username': user.username,
#                         'email': user.email, 
#                         'message': 'Please do not skip the last step to verify your account.'
#                     }
#                 return Responses.response_api('Register Successfull','200 OK' , data = data)

#         except Exception as e:
#             return Responses.response_api('str(e)','401 Unauthorized' , error = str(e))
    
#     @action(detail= False , methods=['POST'])
#     def customer_login(self, request): 
#         data = request.data 
#         serializer = CustomerSignUp(data=data)
#         try:
#             if serializer.is_valid():
#                 email = data.get('email')
#                 password = data.get('password')
#                 user = authenticate(email=email, password=password)
#                 if user is None: 
#                     return Responses.response_api("Email or password is not valid", "401 Unauthorized")
                
#                 return Responses.response_api("Login Successful", "200 OK")
#             else:
#                 return Responses.response_api("Invalid data", "400 Bad Request", error=serializer.errors)
                    
#         except Exception as e: 
#             return Responses.response_api(str(e), "500 Internal Server Error", error=str(e))

# create new customer account 
class CustomerRegister(generics.CreateAPIView):
    queryset = CustomerAccount.objects.all() 
    serializer_class = CustomerAccountSerializer

class CreateManagerAccount(generics.CreateAPIView):
    queryset = ManagerAccount.objects.all() 
    serializer_class = MangerAccountSerializer
    
class ManagementEmployeeViewset(viewsets.ModelViewSet):
    queryset = EmployeeInformation.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsManagerUser]
    
    
    def create(self, request, *args, **kwargs):
        data = request.data 
        serializers = self.serializer_class(data = data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Responses.response_api("Add Employee Successfull","200")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        serializers = self.serializer_class(instance,data , partial = True ) 
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return  Responses.response_api('Update successfully', '200')

# store booking information of customer 
class CustomerBookingViewset(viewsets.ModelViewSet):
    queryset = CustomerBookingInformation.objects.all()
    serializer_class = CustomerBookingInfoSerializer
    permission_classes = [IsAuthenticated | IsLoginManagerOrCustomer]
    def post(self, request):
        data = request.data
        print(data.get('phone_number'))
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Responses.response_api('Booking successfully', '200')
        else:
            return Responses.response_api(serializer.errors, '400')

#store feedback from the user 
class FeedBackFromCustomerViewset(viewsets.ModelViewSet):
    queryset = FeedbackFromCustomer.objects.all() 
    serializer_class = FeedbackFromcustomerSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=False , methods=['POST'])
    def feedback_send_from_user(self, request):
        permission = IsLoginManagerOrCustomer()
        if not permission.has_permission(request, self):
            return Responses.response_api("Permission denied", '403')
        data = request.data
        serializers = FeedbackFromcustomerSerializer(data = data )
        if serializers.is_valid():
            serializers.save(customer = request.user)
            return Responses.response_api("Feedback successfully",'200')
        return Responses.response_api(serializers.errors,'400')
    @action(detail=True,methods=['DELETE'])
    def delete_feedback_user(self, request , pk=None):
        try:
            permission = IsManagerUser()
            if not permission.has_permission(request,self):
                return Responses.response_api("Permission denied","403")
            feedback = self.get_object()
            feedback.delete()
            return Responses.response_api("Delete Feedback succesfull",'200')
        except Exception as e : 
            return Responses.response_api("Error","403", error=str(e))
    # @action(detail=False, methods=['GET'])
    # def get_feedback(self, request):
    #     try: 
    #         permission = IsManagerUser()
    #         if not permission.has_permission(request,self):
    #             return Responses.response_api("Permission denied","403")
    #         feedback = self.queryset
    #         serializers = self.serializer_class(feedback , many= True)
    #         print(serializers.data)
    #         return Responses.response_api("Get feedback successfull",'200',data = serializers.data)
    #     except Exception as e : 
    #         return Responses.response_api("Error","400",error=str(e)) 

class ManagementProduct(viewsets.ModelViewSet):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes=[IsManagerUser]

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object() 
        serializers = self.serializer_class(instance, data, partial = True)
        serializers.is_valid(raise_exception=True)
        serializers.save() 
        return Responses.response_api('Update product successfully') 

# class ShowItemInMenu()
class ShowItemIntoMenu(viewsets.ModelViewSet):
    queryset= MenuItems.objects.all() 
    serializer_class = MenuItemSerializer
        
    def get(self, request , pk = None):
        try: 
            if pk is None:
                item = MenuItems.objects.all()
                print(item)
                serializers = MenuItemSerializer(item , many = True)
                return Responses.response_api("Fetch Item successfully","200", data = serializers.data)
            else: 
                item = self.get_object()
                serializers = MenuItemSerializer(item)
                return Responses.response_api("Fetch Item successfully","200", data = serializers.data)
            
        except Exception as e:
            return Responses.response_api("Error","400",error=str(e))
        
        
# class OrderCreateView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self , request):
#         print(request.user)
#         print(request.data)
#         serializers = OrderSerializer(data = request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Responses.response_api("Successfull",'200',data = serializers.data)
#         else : 
            
#             print(serializers.errors)

#         return Responses.response_api("Unsuccessfull","400")



        
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all() 
    permission_classes = [IsAuthenticated]
    def create(self, request):
        customer_id = request.data.get('customer')
        customer = CustomerAccount.objects.get(id=customer_id) 
        menu_item_id = request.data.get('menu_item')
        quantity = int(request.data.get('quantity'))

        menu_item = MenuItems.objects.get(id=menu_item_id)
        cart, created = Cart.objects.get_or_create(customer=customer)
        
     
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults={  # use default to make quantity not change => not create new cart item when same item was added
                    'quantity': quantity,
                    'price': menu_item.price * quantity
                }
        )
        if not created:
            cart_item.quantity += quantity
        cart_item.price = menu_item.price * cart_item.quantity
        cart_item.save()

        return Responses.response_api('Item added to cart','200_OK')

    


class CartDetailView(APIView):
    permission_classes = [IsLoginManagerOrCustomer]
    def get(self, request):
        try:
            customer_id = request.query_params.get('customer')  
            if not customer_id:
                return Responses.response_api(
                    "Customer ID is required.", 
                    "400"
                )

            customer = CustomerAccount.objects.get(id=customer_id)
            print(customer)
            cart = Cart.objects.filter(customer=customer).first()
            
            if not cart:
                return Responses.response_api(
                    "No cart found for this customer.",
                    "404"
                )

           
            serializer = CartSerializer(cart)
            
            return Responses.response_api(
                "Fetch items successfully.",
                "200", data=serializer.data
            )
        except Exception as e:
            return Responses.response_api(
                "Error" , " 400" , error=str(e)
            )
            
            
class CreateOrderView(APIView): 
    permission_classes = [IsAuthenticated]
    def post(self, request): 
        try:
            total_price = 0 
            customer_id = request.query_params.get('customer')
            customer = CustomerAccount.objects.get(id = customer_id)
            cart = Cart.objects.filter(customer = customer).first()
            if not cart or not cart.items.exists():
                return Responses.response_api("Item not exists","400")
            
            items = cart.items.all() 
            for item in items: 
                total_price += item.price 
                
            order = Order.objects.create(
                customer = customer, 
                total_price = total_price
            )
            
            for item in items: 
                OrderItem.objects.create(
                    order = order, 
                    menu_item = item.menu_item, 
                    quantity = item.quantity , 
                    price = item.price 
                )

            cart.items.all().delete()
            return Responses.response_api("Order create succesfully","200")
            
        except Exception as e : 
            return Responses.response_api("Error","403",error= str(e))
        
    
class GoogleSignInView(generics.GenericAPIView):
    serializer_class = GoogleSignInSerializer
    
    def post(self , request):
      
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['access_token'])
        return Responses.response_api("Successfull","200 OK", data=data )