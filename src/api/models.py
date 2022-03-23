from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    publisher_name = models.CharField(max_length=512, blank=False, null=False, help_text='Wydawnictwo')
    author_name = models.CharField(max_length=512, blank=False, null=False, help_text='Autor')
    title = models.CharField(max_length=512, blank=False, null=False, help_text='Tytuł')
    publication_year = models.PositiveIntegerField(blank=True, null=True, help_text='Rok publikacji')
    publication_number = models.PositiveIntegerField(blank=True, null=True, help_text='Nr wydania książki')
    comment = models.TextField(blank=True, null=True, help_text='Komentarz użytkownika do książki')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Data i czas utworzenia pozycji')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, help_text='Użytkownik, który utworzył pozycję')

    def __str__(self):
        return f"{self.title ({self.author})}"

    class Meta:
        verbose_name = 'Książka'
        verbose_name_plural = 'Książki'
        db_table = "bookapp_books"
