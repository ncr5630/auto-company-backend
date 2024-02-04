from django.urls import path
from .views import (
        CategoryListCreateView, CategoryDetailView,
        ProductListView, ProductDetailView,
        MasterStockListView, MasterStockDetailView,
        OrderListView, OrderDetailView, OrderItemCreateView
        )

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<int:category_id>/', CategoryDetailView.as_view(), name='category_detail'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('masterstock/', MasterStockListView.as_view(), name='master_stock_list'),
    path('masterstock/<int:master_stock_id>/', MasterStockDetailView.as_view(), name='master_stock_detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/items/', OrderItemCreateView.as_view(), name='order-item-create'),

]
