from django.db import models


class Shop(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=200, db_index=True)
    email = models.CharField(max_length=200, db_index=True)
    about = models.TextField()

    def __str__(self):
        return f'{self.address} - {self.phone} - {self.email}'


class ShopStory(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    subtitle = models.CharField(max_length=200, db_index=True)
    story = models.TextField()

    def __str__(self):
        return f'{self.title} - {self.subtitle}'


class ShopTestimonial(models.Model):
    image = models.ImageField(upload_to='shop/features', blank=True)
    name = models.CharField(max_length=200, db_index=True)
    position = models.CharField(max_length=200, db_index=True)
    testimony = models.TextField()

    def __str__(self):
        return self.name
