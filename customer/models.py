from django.db import models
from django.utils import timezone

class Customer(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Remove', 'Remove'),
    ]

    id = models.AutoField(primary_key=True)
    customerCode = models.CharField(max_length=20, unique=True, editable=False)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField(max_length=100)
    cusName = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    createdAt = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.customerCode:
            # Generate a new customerCode only if it's a new record
            last_customer = Customer.objects.order_by('id').last()
            if last_customer:
                self.customerCode = f"CU{str(last_customer.id + 1).zfill(8)}"
            else:
                self.customerCode = f"CU{str(1).zfill(8)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cusName
