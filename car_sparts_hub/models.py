from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from customer.models import Customer
class Category(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    id = models.AutoField(primary_key=True)
    pid = models.IntegerField()
    name = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('Number', 'Number'),
        ('kg', 'kg'),
        ('Lt', 'Lt'),
        ('Bags', 'Bags'),
        ('Pcs', 'Pcs'),
        ('Mt', 'Mt'),
        ('Boxes', 'Boxes'),
    ]

    id = models.AutoField(primary_key=True)
    productCord = models.CharField(max_length=20, unique=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    productName = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    productUnits = models.CharField(max_length=10, choices=UNIT_CHOICES)
    unitCost = models.DecimalField(max_digits=10, decimal_places=2)
    profitPercentage = models.DecimalField(max_digits=10, decimal_places=2)
    sellingPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.CharField(max_length=250)
    status = models.CharField(max_length=10, choices=Category.STATUS_CHOICES)

    def __str__(self):
        return self.productName

    def calculate_selling_price(self):
        if self.unitCost is not None and self.profitPercentage is not None:
            return self.unitCost + (self.unitCost * self.profitPercentage / 100)
        return None

    def save(self, *args, **kwargs):
        if not self.productCord:
            last_product = Product.objects.order_by('id').last()
            if last_product:
                self.productCord = f"PRO{str(last_product.id + 1).zfill(8)}"
            else:
                self.productCord = f"PRO{str(1).zfill(8)}"
        super().save(*args, **kwargs)


class MasterStock(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    totalStock = models.DecimalField(max_digits=10, decimal_places=2)
    totalPurchase = models.DecimalField(max_digits=10, decimal_places=2)
    totalSelling = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text='This value is for selling items only')
    lastUpdated = models.DateTimeField(auto_now=True)
    lastUpdateBy = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.category.name} - {self.product.productName}"

    class Meta:
        unique_together = ['category', 'product']


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        if self.quantity:
            unit_price = self.product.sellingPrice
            if unit_price:
                self.unit_price = unit_price
                self.subtotal = self.unit_price * self.quantity

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.productName} - Subtotal: {self.subtotal}"

