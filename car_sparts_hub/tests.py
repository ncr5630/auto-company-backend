from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Product, MasterStock, Order, OrderItem
from .serializers import (CategorySerializer, ProductSerializer,
                          MasterStockSerializer, OrderSerializer, OrderItemSerializer)

class CategoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_category(self):
        data = {'pid':0, 'name': 'Test Category', 'status': 'Active'}
        response = self.client.post('/api/categories/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Test Category')

    def test_get_categories(self):
        Category.objects.create(pid=0, name='Category 1', status='Active')
        Category.objects.create(pid=0, name='Category 2', status='Inactive')

        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['categories']), 2)


class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(pid=1, name='Test Category', status='Active')

    def test_create_product(self):
        data = {
            'productName': 'Test Product',
            'description': 'Test Description',
            'productUnits': 'Number',
            'unitCost': 100,
            'profitPercentage': 25,
            'sellingPrice': 125,
            'createdBy': 'Test User',
            'status': 'Active',
            'category': self.category.id
        }
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().productName, 'Test Product')

    def test_get_products(self):
        Product.objects.create(
            productName='Product 1',
            description='Description 1',
            productUnits='Number',
            unitCost=100,
            profitPercentage=25,
            sellingPrice=125,
            createdBy='User 1',
            status='Active',
            category=self.category
        )
        Product.objects.create(
            productName='Product 2',
            description='Description 2',
            productUnits='Number',
            unitCost=150,
            profitPercentage=30,
            sellingPrice=195,
            createdBy='User 2',
            status='Inactive',
            category=self.category
        )

        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['products']), 2)

# Similar tests can be created for MasterStock, Order, OrderItem views
