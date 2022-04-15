from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

def upload_to(instance, filename):
    return 'covers/{filename}'.format(filename=filename)

class Book(models.Model):
    class Status(models.IntegerChoices):
        TO_READ = 0, ('do przeczytania')
        IN_PROGRESS = 1, ('w trakcie')
        READ = 2, ('przeczytana')
   
    publisher_name = models.CharField(max_length=512, blank=False, null=False, help_text='Wydawnictwo')
    author_name = models.CharField(max_length=512, blank=False, null=False, help_text='Autor')
    title = models.CharField(max_length=512, blank=False, null=False, help_text='Tytuł')
    publication_year = models.PositiveIntegerField(blank=True, null=True, help_text='Rok publikacji')
    publication_number = models.PositiveIntegerField(blank=True, null=True, help_text='Nr wydania książki')
    comment = models.TextField(blank=True, null=True, help_text='Komentarz użytkownika do książki')
    rate = models.PositiveSmallIntegerField(blank=True, default=0, help_text='Ocena użytkownika (min=0, max=5)', validators=[MinValueValidator(0), MaxValueValidator(5)])
    status = models.PositiveSmallIntegerField(blank=True, null=True, choices=Status.choices, help_text='Status książki: 0-do przeczytania, 1-w trakcie, 2-przeczytana')
    cover = models.ImageField(blank=True, null=True, upload_to=upload_to, help_text='Okładka książki')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Data i czas utworzenia pozycji')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, help_text='Użytkownik, który utworzył pozycję')
    
    def __str__(self):
        return f"{self.title} ({self.author})"

    class Meta:
        verbose_name = 'Książka'
        verbose_name_plural = 'Książki'
        db_table = "bookapp_books"
