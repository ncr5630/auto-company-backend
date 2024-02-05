from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import (Category, Product, MasterStock, Order, OrderItem)
from .serializers import (CategorySerializer, ProductSerializer, ProductCreateSerializer,
                          MasterStockSerializer, MasterCreateStockSerializer,
                          OrderSerializer, OrderItemSerializer, OrderCreateSerializer,
                          OrderItemCreateSerializer
                          )
from django.shortcuts import get_object_or_404


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


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListCreateView(APIView):
    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={status.HTTP_201_CREATED: CategorySerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CategorySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({'categories': serializer.data})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(APIView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CategorySerializer}
    )
    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, pk=category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={status.HTTP_200_OK: CategorySerializer}
    )
    def put(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, pk=category_id)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: 'Category deleted successfully'}
    )
    def delete(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, pk=category_id)
        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ProductListView(APIView):
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ProductSerializer(many=True)},
        manual_parameters=pagination_params,
    )
    def get(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        products = Product.objects.order_by('id')
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', self.pagination_class.page_size)

        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response({'products': serializer.data})

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: ProductSerializer()},
        request_body=ProductCreateSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ProductSerializer()},
    )
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ProductSerializer()},
        request_body=ProductSerializer
    )
    def put(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: 'Product deleted successfully'},
    )
    def delete(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class MasterStockListView(APIView):
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: MasterStockSerializer(many=True)},
        manual_parameters=pagination_params,
    )
    def get(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        master_stock = MasterStock.objects.order_by('id')
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', self.pagination_class.page_size)

        result_page = paginator.paginate_queryset(master_stock, request)
        serializer = MasterStockSerializer(result_page, many=True)
        return paginator.get_paginated_response({'master_stock': serializer.data})

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: MasterStockSerializer()},
        request_body=MasterCreateStockSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = MasterCreateStockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MasterStockDetailView(APIView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: MasterStockSerializer()},
    )
    def get(self, request, master_stock_id, *args, **kwargs):
        master_stock = get_object_or_404(MasterStock, pk=master_stock_id)
        serializer = MasterStockSerializer(master_stock)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: MasterStockSerializer()},
        request_body=MasterStockSerializer
    )
    def put(self, request, master_stock_id, *args, **kwargs):
        master_stock = get_object_or_404(MasterStock, pk=master_stock_id)
        serializer = MasterStockSerializer(master_stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: 'MasterStock deleted successfully'},
    )
    def delete(self, request, master_stock_id, *args, **kwargs):
        master_stock = get_object_or_404(MasterStock, pk=master_stock_id)
        master_stock.delete()
        return Response({'message': 'MasterStock deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        responses={200: OrderSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: OrderSerializer()},
        request_body=OrderCreateSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        responses={200: OrderSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={200: OrderSerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={200: OrderSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    @swagger_auto_schema(
        request_body=OrderItemCreateSerializer,
        responses={201: OrderItemSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(pk=order_id)
        serializer.save(order=order)
