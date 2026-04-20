from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()


class RegisterView(generics.CreateAPIView):
	"""
	Register a new user account.
	Accepts username, email, and password in the request body.
	"""
	queryset = User.objects.all()
	serializer_class = RegisterSerializer
	permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
	"""
	User login endpoint. Returns access and refresh JWT tokens.
	Accepts username and password.
	"""
	permission_classes = [permissions.AllowAny]
