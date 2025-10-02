from django.test import TestCase


class SimpleTest(TestCase):
    def test_addition(self):
        """Testa se 1 + 1 é igual a 2."""
        self.assertEqual(1 + 1, 2)
