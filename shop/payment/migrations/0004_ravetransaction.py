# Generated by Django 3.1.5 on 2023-01-14 22:16

from django.db import migrations, models
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_mpesatransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='RaveTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_id', models.CharField(default=uuid.uuid4, max_length=50, unique=True)),
                ('tx_reference', models.CharField(default=uuid.uuid4, max_length=50, unique=True)),
                ('status', models.CharField(choices=[(1, 'successful'), (0, 'failed')], default=0, max_length=15)),
                ('amount', models.CharField(max_length=10)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]