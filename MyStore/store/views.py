from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
import jwt
from datetime import datetime, timedelta
from .authentication import JwtAuthentication
from .models import Product
from .serializers import UserCreateSerializer, UserListSerializer, UserUpdateSerializer, UserAuthSerializer, \
    ProductSerializer, ProductDetailsSerializer
from django.conf import settings


@api_view(["GET"])
def echo(request):
    return Response(data="OK", status=status.HTTP_200_OK)


class RegisterAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response(data={"message": "created"}, status=response.status_code)
        else:
            return response


class UsersListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JwtAuthentication]
    serializer_class = UserListSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserGetAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class AuthAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication Token'),
                }
            ),
            401: 'Unauthorized'
        },
    )
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data["username"],
                            password=serializer.validated_data["password"])
        if user:
            token = jwt.encode({"id": user.id,
                                "exp": datetime.now() + timedelta(minutes=settings.AUTH_EXPIRATION),
                                "admin": user.is_superuser},
                               key=settings.AUTH_SECRET_KEY,
                               algorithm=settings.AUTH_ALGORITHM)
            return Response(data={"token": token}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class ProductCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
