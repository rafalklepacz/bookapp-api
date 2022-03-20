from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    firstname = models.CharField(max_length=256, blank=False, null=False, help_text='Imię autora')
    lastname = models.CharField(max_length=512, blank=False, null=False, help_text='Nazwisko autora')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Data i czas utworzenia pozycji')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, help_text='Użytkownik, który utworzył pozycję')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        unique_together = ('firstname', 'lastname')
        verbose_name = 'Autor'
        verbose_name_plural = 'Autorzy'
        db_table = "bookapp_authors"


class Publisher(models.Model):
    name = models.CharField(max_length=512, blank=False, null=False, unique=True, help_text='Nazwa wydawnictwa')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Data i czas utworzenia pozycji')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, help_text='Użytkownik, który utworzył pozycję')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Wydawnictwo'
        verbose_name_plural = 'Wydawnictwa'
        db_table = "bookapp_publishers"


class Book(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, help_text='Wydawca książki')
    authors = models.ManyToManyField(Author, related_name="book_list", help_text='Autor książki')
    title = models.CharField(max_length=512, blank=False, null=False, help_text='Tytuł książki')
    publication_year = models.PositiveIntegerField(blank=True, null=True, help_text='Rok publikacji książki')
    publication_number = models.PositiveIntegerField(blank=True, null=True, help_text='Nr wydania książki')
    comment = models.TextField(blank=True, null=True, help_text='Komentarz użytkownika do książki')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Data i czas utworzenia pozycji')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, help_text='Użytkownik, który utworzył pozycję')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Książka'
        verbose_name_plural = 'Książki'
        db_table = "bookapp_books"
