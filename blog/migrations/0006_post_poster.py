# Generated by Django 3.1.5 on 2023-01-08 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20230108_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='poster',
            field=models.ImageField(blank=True, upload_to='blog'),
        ),
    ]
