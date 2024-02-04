from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer

class CustomerAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_customer(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
            "contactNumber": "1234567890",
            "address": "Test Address",
            "email": "test@example.com",
            "cusName": "Test Customer",
            "description": "Test description",
            "status": "Active",
        }

        response = self.client.post('/api/customers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        customer = Customer.objects.get(id=response.data['id'])
        self.assertEqual(customer.cusName, 'Test Customer')

    def test_get_customer_list(self):
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer_detail(self):
        customer = Customer.objects.create(
            username="testuser",
            password="testpassword",
            contactNumber="1234567890",
            address="Test Address",
            email="test@example.com",
            cusName="Test Customer",
            description="Test description",
            status="Active",
        )

        response = self.client.get(f'/api/customers/{customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cusName'], 'Test Customer')

    def test_update_customer(self):
        customer = Customer.objects.create(
            username="testuser",
            password="testpassword",
            contactNumber="1234567890",
            address="Test Address",
            email="test@example.com",
            cusName="Test Customer",
            description="Test description",
            status="Active",
        )

        updated_data = {
            "username": "testuser",
            "password": "testpassword",
            "contactNumber": "1234567890",
            "address": "Updated Address",
            "email": "test@example.com",
            "cusName": "Updated Customer",
            "description": "Updated description",
            "status": "Inactive",
        }

        response = self.client.put(f'/api/customers/{customer.id}/', updated_data, format='json')

        if response.status_code != status.HTTP_200_OK:
            print(f"Response content: {response.content.decode('utf-8')}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_customer = Customer.objects.get(id=customer.id)
        self.assertEqual(updated_customer.cusName, 'Updated Customer')
        self.assertEqual(updated_customer.status, 'Inactive')

    def test_delete_customer(self):
        customer = Customer.objects.create(
            username="testuser",
            password="testpassword",
            contactNumber="1234567890",
            address="Test Address",
            email="test@example.com",
            cusName="Test Customer",
            description="Test description",
            status="Active",
        )

        response = self.client.delete(f'/api/customers/{customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Customer.DoesNotExist):
            Customer.objects.get(id=customer.id)
