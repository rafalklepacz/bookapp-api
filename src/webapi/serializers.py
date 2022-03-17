from rest_framework import serializers
from .models import Publisher, Author, Book


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "publisher", "authors", "title", "publication_year",
                  "publication_number", "comment"]


class AuthorSerializer(serializers.ModelSerializer):
    book_list = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "firstname", "lastname", "book_list"]
