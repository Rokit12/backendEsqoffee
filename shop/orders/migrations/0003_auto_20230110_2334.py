# Generated by Django 3.1.5 on 2023-01-10 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=30, verbose_name='phone'),
        ),
    ]