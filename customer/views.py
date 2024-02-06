from rest_framework import generics
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


pagination_params = [
    openapi.Parameter(
        'page',
        openapi.IN_QUERY,
        description='Page number',
        type=openapi.TYPE_INTEGER,
        default=1,
    ),
    openapi.Parameter(
        'page_size',
        openapi.IN_QUERY,
        description='Number of items per page',
        type=openapi.TYPE_INTEGER,
        default=CustomPageNumberPagination.page_size,
    ),
]

class CustomerListCreateView(generics.ListCreateAPIView):
    pagination_class = CustomPageNumberPagination
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @swagger_auto_schema(
        responses={200: CustomerSerializer(many=True)},
        manual_parameters=pagination_params,
    )
    def get(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        customers = Customer.objects.order_by('id')
        result_page = paginator.paginate_queryset(customers, request)
        serializer = CustomerSerializer(result_page, many=True)
        return paginator.get_paginated_response({'customers': serializer.data})

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
