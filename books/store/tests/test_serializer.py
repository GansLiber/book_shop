from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')

    def test_ok(self):
        book_1 = Book.objects.create(name='Book gg 1', price=24, authtor_name='Autor 1', owner=self.user)
        book_2 = Book.objects.create(name='Book gg 2', price=224, authtor_name='Autor 2', owner=self.user)
        data = BookSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Book gg 1',
                'price': '24.00',
                'authtor_name': 'Autor 1',
                'owner': self.user.id
            },
            {
                'id': book_2.id,
                'name': 'Book gg 2',
                'price': '224.00',
                'authtor_name': 'Autor 2',
                'owner': self.user.id
            }
        ]
        data = [dict(item) for item in data]
        # self.assertEqual(expected_data, data)
