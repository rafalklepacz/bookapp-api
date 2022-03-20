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
    """
    list:
    Zwraca listę wszystkich wydawnictw dodanych przez wszystkich użytkowników, na podstawie kryteriów filtrowania podanych przez użytkownika.
    
    Parametry filtrowania:<br/>
    `name__icontains` - nazwa wydawnictwa
    
    create:
    Umożliwia dodanie nowego wydawnictwa
    
    retrieve:
    Zwraca szczegółowe dane wydawnictwa o danym ID

    update:
    Umożliwia aktualizację danych wydawnictwa o podanym ID

    destroy:
    Umożliwia usunięcie wydawnictwa o danym ID
    """
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
    """
    list:
    Zwraca listę wszystkich autorów dodanych przez wszystkich użytkowników, na podstawie kryteriów filtrowania podanych przez użytkownika.
    
    Parametry filtrowania:<br/>
    `firstname__icontains` - imię autora,<br/>
    `lastname__icontains` - nazwisko autora
    
    create:
    Umożliwia dodanie nowego autora
    
    retrieve:
    Zwraca szczegółowe dane autora o danym ID

    update:
    Umożliwia aktualizację danych autora o podanym ID

    destroy:
    Umożliwia usunięcie autora o danym ID
    """
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
    """
    list:
    Zwraca listę wszystkich książek dodanych przez aktualnie zalogowanego użytkownika, na podstawie kryteriów filtrowania podanych przez użytkownika.
    
    Parametry filtrowania:<br/>
    `publisher__name__icontains` - nazwa wydawnictwa,<br/>
    `authors__firstname__icontains` - imię autora,,<br/>
    `authors__lastname__icontains` - nazwisko autora,,<br/>
    `title__icontains` - tytuł książki,,<br/>
    `publication_year` - rok publikacji książki,,<br/>
    `publication_number` - nr wydania książki
    
    create:
    Umożliwia dodanie nowej książki
    
    retrieve:
    Zwraca szczegółowe dane książki o danym ID

    update:
    Umożliwia aktualizację danych książki o podanym ID

    destroy:
    Umożliwia usunięcie książki o danym ID
    """
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
    """
    list:
    Zwraca dane aktualnie zalogowanego użytkownika
    
    create:
    Umożliwia utworzenie nowego użytkownika
    
    retrieve:
    Zwraca dane aktualnie zalogowanego użytkownika
    """
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
