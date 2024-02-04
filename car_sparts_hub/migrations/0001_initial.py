# Generated by Django 5.0.1 on 2024-02-03 10:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pid', models.IntegerField()),
                ('name', models.CharField(max_length=200, unique=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('invoiceCode', models.CharField(max_length=20)),
                ('grossTotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discountPercentage', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discountAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('netTotal', models.DecimalField(decimal_places=2, help_text='This is the final bill amount for the sale', max_digits=10)),
                ('totalProfit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paidAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dueAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balanceToPay', models.DecimalField(decimal_places=2, max_digits=10)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
                ('createdBy', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Completed', 'Completed'), ('Pending', 'Pending')], max_length=10)),
                ('customerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('productCord', models.CharField(max_length=20)),
                ('productName', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('productUnits', models.CharField(choices=[('Number', 'Number'), ('kg', 'kg'), ('Lt', 'Lt'), ('Bags', 'Bags'), ('Pcs', 'Pcs'), ('Mt', 'Mt'), ('Boxes', 'Boxes')], max_length=10)),
                ('unitCost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('profitPercentage', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sellingPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('createdBy', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_sparts_hub.category')),
            ],
        ),
        migrations.CreateModel(
            name='ordersDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sellQty', models.IntegerField()),
                ('unitPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sellingPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subTotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subTotalProfit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('createDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('OrderMasterId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_sparts_hub.ordermaster')),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_sparts_hub.product')),
            ],
        ),
        migrations.CreateModel(
            name='MasterStock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('totalStock', models.DecimalField(decimal_places=2, max_digits=10)),
                ('totalPurchase', models.DecimalField(decimal_places=2, max_digits=10)),
                ('totalSelling', models.DecimalField(decimal_places=2, help_text='This value is for selling items only', max_digits=10)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
                ('lastUpdateBy', models.CharField(max_length=250)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_sparts_hub.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_sparts_hub.product')),
            ],
        ),
    ]
