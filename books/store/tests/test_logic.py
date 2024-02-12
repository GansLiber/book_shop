from django.test import TestCase

from store.logic import operations


class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(5, 7, '+')
        self.assertEqual(12, result)

    def test_minus(self):
        result = operations(5, 7, '-')
        self.assertEqual(-2, result)

    def test_multiply(self):
        result = operations(5, 7, '*')
        self.assertEqual(35, result)
