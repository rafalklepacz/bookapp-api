from django.db.models import ProtectedError
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet

from .models import Publisher, Author, Book
from .serializers import UserSerializer, PublisherSerializer, AuthorSerializer, BookSerializer
from .authentication import TokenAuthentication


class PublisherView(ModelViewSet):
    serializer_class = PublisherSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Publisher.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"name": ["icontains"]}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, pk=None):
        publisher = get_object_or_404(Publisher, id=pk)
        try:
            publisher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            errorMsg = f"Cannot delete the publisher '{publisher.name}' because is referenced to some book."
            return Response(data={'message': errorMsg}, status=status.HTTP_400_BAD_REQUEST)


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"publisher__name": ["icontains"],
                        "authors__firstname": ["icontains"],
                        "authors__lastname": ["icontains"],
                        "title": ["icontains"],
                        "publication_year": ["exact"],
                        "publication_number": ["exact"]}

    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    permission_classes_by_action = {'create': [permissions.AllowAny]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
        
    def get_object(self):
        return self.request.user

    def get(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)

    def list(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)
