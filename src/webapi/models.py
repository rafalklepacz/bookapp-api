from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    firstname = models.CharField(max_length=256, blank=False, null=False)
    lastname = models.CharField(max_length=512, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autorzy'
        db_table = "bookapp_authors"


class Publisher(models.Model):
    name = models.CharField(max_length=512, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Wydawnictwo'
        verbose_name_plural = 'Wydawnictwa'
        db_table = "bookapp_publishers"


class Book(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT)
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=512, blank=False, null=False)
    publication_year = models.PositiveIntegerField(blank=True, null=True)
    publication_number = models.PositiveIntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        verbose_name = 'Książka'
        verbose_name_plural = 'Książki'
        db_table = "bookapp_books"
