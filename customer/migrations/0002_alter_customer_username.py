# Generated by Django 5.0.1 on 2024-02-03 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]