from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.viewsets import ViewSet, ModelViewSet
from .models import Publisher, Author, Book
from .serializers import PublisherSerializer, AuthorSerializer, BookSerializer
from .authentication import TokenAuthentication


class PublisherView(ViewSet):
    serializer_class = PublisherSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Publisher.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"name": ["icontains"]}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AuthorView(ModelViewSet):
    serializer_class = AuthorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Author.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"firstname": ["icontains"],
                        "lastname": ["icontains"]}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BookView(ModelViewSet):
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"publisher__name": ["icontains"],
                        "authors__firstname": ["icontains"],
                        "authors__lastname": ["icontains"],
                        "title": ["icontains"],
                        "publication_year": ["exact"],
                        "publication_number": ["exact"]}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
