from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product

class ProductAPITests(APITestCase):
    def setUp(self):
        self.valid_payload = {
            "name": "Kelas Belajar Python",
            "sku": "DCD01",
            "description": "This is a sample description.",
            "shop": "Dicoding",
            "location": "Bandung",
            "price": 1500000,
            "discount": 0,
            "category": "Course",
            "stock": 1000,
            "is_available": True,
            "picture": "https://www.shutterstock.com/image-vector/sample.jpg"
        }
        self.product = Product.objects.create(**self.valid_payload)

    def test_create_product(self):
        response = self.client.post(reverse('product-list-create'), data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_products(self):
        response = self.client.get(reverse('product-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)