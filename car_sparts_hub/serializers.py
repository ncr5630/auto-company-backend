from rest_framework import serializers
from .models import Category, Product, MasterStock, Order, OrderItem
from customer.models import Customer
from customer.serializers import CustomerSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['sellingPrice']  # Exclude 'sellingPrice' from the creation schema

    def create(self, validated_data):
        # Calculate 'sellingPrice' before saving
        unit_cost = validated_data.get('unitCost')
        profit_percentage = validated_data.get('profitPercentage')

        if unit_cost is not None and profit_percentage is not None:
            validated_data['sellingPrice'] = unit_cost + (unit_cost * profit_percentage / 100)

        # Create the product
        return Product.objects.create(**validated_data)


class MasterCreateStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = MasterStock
        fields = '__all__'

    def create(self, validated_data):
        # Create the MasterStock instance
        master_stock_instance = MasterStock.objects.create(**validated_data)

        return master_stock_instance


class MasterStockSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product = ProductSerializer()

    class Meta:
        model = MasterStock
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'delivery_date', 'is_ordered', 'created_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
    def create(self, validated_data):
        return Order.objects.create(**validated_data)


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']  # Only include the necessary fields

    def create(self, validated_data):
        quantity = validated_data['quantity']
        product_id = validated_data.get('product')
