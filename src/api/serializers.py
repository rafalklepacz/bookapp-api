from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Profile


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "publisher_name", "author_name", "title", "publication_year",
                  "publication_number", "comment", "rate", "status", "cover"]

class ProfileSerializer(serializers.Serializer):
    model = Profile

    plan_to_read = serializers.CharField(required=False)

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
