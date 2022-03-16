from rest_framework import serializers
from . import models


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publisher
        fields = ["id", "name"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ["id", "firstname", "lastname"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = ["id", "publisher", "authors", "title", "publication_year",
                  "publication_number", "comment", "created_at"]
