from functools import partial
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import UserSerializer, BookSerializer, ChangePasswordSerializer
from .authentication import TokenAuthentication


class BookView(ModelViewSet):
    """
    list:
    Zwraca listę wszystkich książek dodanych przez aktualnie zalogowanego użytkownika, na podstawie kryteriów filtrowania podanych przez użytkownika.

    Parametry filtrowania:<br/>
    `publisher_name__icontains` - nazwa wydawnictwa,<br/>
    `author_name__icontains` - nazwa autora,<br/>
    `title__icontains` - tytuł książki,,<br/>
    `publication_year__gte` - rok publikacji książki większy lub równy od,<br/>
    `publication_year__lte` - rok publikacji książki mniejszy lub równy od,<br/>
    `publication_year` - dokładny rok publikacji książki,<br/>
    `publication_number__gte` - nr wydania książki większy lub równy od,<br/>
    `publication_number__lte` - nr wydania książki mniejszy lub równy od,<br/>
    `publication_number` - dokładny nr wydania książki,<br/>
    `status__in` - status książki zawiera się w przekazanej liście (wartości oddzielone przecinkami: np.: /?status__in=1,2),<br/>
    `status` - dokładny status książki,<br/>
    `rate__gte` - ocena książki większa lub równa od,<br/>
    `rate__lte` - ocena książki mniejsza lub równa od,<br/>
    `rate` - dokładna ocena książki

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
    #parser_classes = (FormParser, MultiPartParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'publisher_name': ['icontains'],
                        'author_name': ['icontains'],
                        'title': ['icontains'],
                        'publication_year': ['gte', 'lte', 'exact'],
                        'publication_number': ['gte', 'lte', 'exact'],
                        'status': ['in', 'exact'],
                        'rate': ['gte', 'lte', 'exact']}

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
    
    update:
    Umożliwia zmianę hasła użytkownika

    retrieve:
    Zwraca dane aktualnie zalogowanego użytkownika
    """
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    permission_classes_by_action = {'create': [permissions.AllowAny]}
    
    def get_serializer_class(self):
        if self.action == 'update':
            return ChangePasswordSerializer

        return UserSerializer

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
    
    def update(self, request):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Stare hasło jest nieprawidłowe."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)
