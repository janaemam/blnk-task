from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from .serializers import CustomerRegistrationSerializer, LoginSerializer
from .permissions import IsBankPersonnel, IsCustomer, IsFundProvider
from .models import User


class CustomerRegisterView(CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        request.data['is_bank_personnel'] = False
        request.data['is_fund_provider'] = False
        response = super(). create(request, *args, **kwargs)

        user = User.objects.get(username=request.data['username'])
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Registration successful',
            'token': token.key,
            'role': 'customer',
            'name': user.first_name
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                login(request, user)
                return Response({
                    'message': 'Login successful',
                    'role': 'customer' if user.is_customer else 'fund_provider' if user.is_fund_provider else 'bank_personnel',
                    'name' : user.first_name
                })
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
class CustomerHomeView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Welcome Customer!"})

class FundProviderHomeView(APIView):
    permission_classes = [IsAuthenticated, IsFundProvider]

    def get(self, request, *args, **kwargs):
        
        return Response({"message": "Welcome Fund Provider!"})

class BankPersonnelHomeView(APIView):
    permission_classes = [IsAuthenticated, IsBankPersonnel]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Welcome Bank Personnel!"})
    

class CheckAuthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user = request.user
        role = 'customer' if user.is_customer else 'fund_provider' if user.is_fund_provider else 'bank_personnel'
        return Response({'role': role})