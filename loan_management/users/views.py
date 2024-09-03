from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .serializers import CustomerRegistrationSerializer, LoginSerializer
from .permissions import IsBankPersonnel, IsCustomer, IsFundProvider


class CustomerRegisterView(CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        request.data['is_bank_personnel'] = False
        request.data['is_fund_provider'] = False
        return super().create(request, *args, **kwargs)

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
                    'role': 'customer' if user.is_customer else 'fund_provider' if user.is_fund_provider else 'bank_personnel'
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
        # Your logic for customer home view
        return Response({"message": "Welcome Customer!"})

class FundProviderHomeView(APIView):
    permission_classes = [IsAuthenticated, IsFundProvider]

    def get(self, request, *args, **kwargs):
        # Your logic for fund provider home view
        return Response({"message": "Welcome Fund Provider!"})

class BankPersonnelHomeView(APIView):
    permission_classes = [IsAuthenticated, IsBankPersonnel]

    def get(self, request, *args, **kwargs):
        # Your logic for bank personnel home view
        return Response({"message": "Welcome Bank Personnel!"})
    

class CheckAuthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user = request.user
        role = 'customer' if user.is_customer else 'fund_provider' if user.is_fund_provider else 'bank_personnel'
        return Response({'role': role})