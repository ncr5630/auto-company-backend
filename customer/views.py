from rest_framework import generics
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Customer
from .serializers import CustomerSerializer

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @swagger_auto_schema(
        responses={200: CustomerSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={201: CustomerSerializer()},
        request_body=CustomerSerializer,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @swagger_auto_schema(
        responses={200: CustomerSerializer()},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: CustomerSerializer()},
        request_body=CustomerSerializer,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={204: 'No Content'},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
