import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    url_book = reverse('book-list')

    def setUp(self):
        self.user = User.objects.create(username='test_username')

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

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(4, Book.objects.all().count())
        url = self.url_book
        data = {
            "name": "Django book wtf!!!",
            "price": 435,
            "authtor_name": "Kakoy to chel"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(5, Book.objects.all().count())

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        self.assertEqual(24, self.book_1.price)
        data = {
            "name": self.book_1.name,
            "price": 255,
            "authtor_name": self.book_1.authtor_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(255, self.book_1.price)

    def test_delete(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        self.assertEqual(4, Book.objects.all().count())
        self.client.force_login(self.user)
        response = self.client.delete(url, content_type='application/json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(3, Book.objects.all().count())
