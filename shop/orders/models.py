from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from django.utils.translation import gettext_lazy as _
from shop.products.models import Product
from shop.coupons.models import Coupon


class Reservation(models.Model):
    first_name = models.CharField(_('first name'), max_length=250)
    last_name = models.CharField(_('last name'), max_length=250)
    date = models.CharField(_('date'), max_length=50)
    time = models.CharField(_('time'), max_length=50)
    phone = models.CharField(_('phone'), max_length=30, blank=False, null=False)
    message = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Order(models.Model):
    PAYMENT_OPTIONS = (
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('card', 'Card'),
    )
    PICKUP_OPTIONS = (
        ('pickup', 'Pickup'),
        ('delivered', 'Delivered'),
    )
    transaction_id = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    phone = models.CharField(_('phone'), max_length=30, blank=False, null=False)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('address'), max_length=250)
    postal_code = models.CharField(_('postal code'), max_length=20)
    city = models.CharField(_('city'), max_length=100)
    paid = models.BooleanField(default=False)
    pickup = models.CharField(max_length=10, choices=PICKUP_OPTIONS, default='pickup')
    payment_option = models.CharField(max_length=10, choices=PAYMENT_OPTIONS, default='mpesa')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * \
            (self.discount / Decimal(100))


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
