from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    url_book = reverse('book-list')
    def setUp(self):
        self.book_1 = Book.objects.create(name='Book test 1', price=24, authtor_name='Autor 1')
        self.book_2 = Book.objects.create(name='Book test 2 Autor 1', price=56, authtor_name='Autor 2')
        self.book_3 = Book.objects.create(name='Book test 3', price=89, authtor_name='Autor 3')
        self.book_4 = Book.objects.create(name='Book test 4', price=123, authtor_name='Autor 4')

    def test_get(self):
        url = self.url_book
        response = self.client.get(url)
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3, self.book_4], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = self.url_book
        response = self.client.get(url, data={'search': 'Autor 1'})
        serializer_data = BookSerializer([self.book_1, self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_sort(self):
        url = self.url_book
        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3, self.book_4], many=True).data
        print('ff', serializer_data)
        print('ff', response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
