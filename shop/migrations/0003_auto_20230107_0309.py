# Generated by Django 3.1.5 on 2023-01-07 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_feature'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='product',
            index_together=None,
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
