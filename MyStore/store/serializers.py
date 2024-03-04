from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .validators import validate_unique_username
from .models import Product, ProductVariant


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=30, required=True, validators=[validate_unique_username])
    password = serializers.CharField(min_length=5, max_length=30, required=True, validators=[validate_password])
    email = serializers.EmailField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "is_superuser", "first_name", "last_name", "email")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_filename")

    class Meta:
        model = Product
        exclude = ["description"]

    def get_filename(self, obj):
        return obj.image.name.lstrip("items_img/")


class ProductDetailsSerializer(serializers.ModelSerializer):
    class ProductVariantSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductVariant
            fields = ["id", "color", "size", "price"]

    image = serializers.SerializerMethodField("get_filename")
    variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_filename(self, obj):
        return obj.image.name
