from django.test import TestCase
from django.contrib.auth.models import User
from webapi.models import Author, Publisher, Book


class PublisherTestCase(TestCase):
    def setUp(self):
        self._user = User.objects.create_user(username='test')
        Publisher.objects.create(name="publisher_1", created_by=self._user)
        Publisher.objects.create(name="publisher_2", created_by=self._user)

    def test_publisher_succesfully_created(self):
        publisher_1: Publisher = Publisher.objects.get(name='publisher_1')
        publisher_2: Publisher = Publisher.objects.get(name='publisher_2')

        self.assertIsNotNone(publisher_1)
        self.assertIsNotNone(publisher_2)
        self.assertEqual(publisher_1.created_by.id, self._user.id)
        self.assertEqual(publisher_2.created_by.id, self._user.id)


class AuthorTestCase(TestCase):
    def setUp(self):
        self._user = User.objects.create_user(username='test')
        Author.objects.create(firstname="firstname_1",
                              lastname='lastname_1', created_by=self._user)
        Author.objects.create(firstname="firstname_2",
                              lastname='lastname_2', created_by=self._user)

    def test_author_succesfully_created(self):
        author_1: Author = Author.objects.get(
            firstname="firstname_1", lastname='lastname_1')
        author_2: Author = Author.objects.get(
            firstname="firstname_2", lastname='lastname_2')

        self.assertIsNotNone(author_1)
        self.assertIsNotNone(author_2)
        self.assertEqual(author_1.created_by.id, self._user.id)
        self.assertEqual(author_2.created_by.id, self._user.id)


class BookTestCase(TestCase):
    def setUp(self):
        self._user = User.objects.create_user(username='test')
        self._publisher = Publisher.objects.create(
            name="publisher_1", created_by=self._user)
        self._author_1 = Author.objects.create(
            firstname="firstname_1", lastname='lastname_1', created_by=self._user)
        self._author_2 = Author.objects.create(
            firstname="firstname_2", lastname='lastname_2', created_by=self._user)

    def test_book_succesfully_created(self):
        book_created: Book = Book.objects.create(publisher=self._publisher, title='title_1', publication_year=2022,
                                                 publication_number=1, comment='comment comment comment', created_by=self._user)
        book_created.authors.set([self._author_1, self._author_2])

        book_got: Book = Book.objects.get(pk=book_created.id)

        self.assertIsNotNone(book_created)
        self.assertIsNotNone(book_got)
        self.assertEqual(book_got.created_by.id, self._user.id)
        self.assertEqual(book_got.title, book_created.title)
        self.assertEqual(book_got.comment, book_created.comment)
        self.assertEqual(book_got.publication_number,
                         book_created.publication_number)
        self.assertEqual(book_got.publication_year,
                         book_created.publication_year)
        self.assertEqual(book_got.authors, book_created.authors)
        self.assertEqual(book_got.publisher.id, book_created.publisher.id)
