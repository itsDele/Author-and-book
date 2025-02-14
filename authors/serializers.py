from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Author
from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    Book_author = BookSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Author

        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "age",
            "gender",
            "password",
            "Book_author",
        ]

    def create(self, validated_data):

        password = validated_data.pop("password")

        author = Author.objects.create(
            **validated_data, password=make_password(password)
        )

        return author


class loginserializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = "the credentials are invalid"
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_active:
                msg = "account is disabled"
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = "must include username and password"
            raise serializers.ValidationError(msg, code="authorization")

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return {
            "user": {
                "username": user.username,
                "first name": user.first_name,
                "last name": user.last_name,
                "email": user.email,
            },
            "access token": access_token,
            "refresh token": refresh_token,
        }
