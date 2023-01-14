import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class MpesaTransaction(models.Model):
    STATUS = (
        (1, "Pending"),
        (0, "Complete")
    )
    """This model records all the mpesa payment transactions"""
    transaction_no = models.CharField(default=uuid.uuid4, max_length=50, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    checkout_request_id = models.CharField(max_length=200)
    reference = models.CharField(max_length=40, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS, default=1)
    receipt_no = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return f"{self.transaction_no}"


class RaveTransaction(models.Model):
    STATUS = (
        (1, "successful"),
        (0, "failed")
    )
    tx_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    tx_reference = models.CharField(default=uuid.uuid4, max_length=50, unique=True)
    status = models.CharField(max_length=15, choices=STATUS, default=0)
    amount = models.CharField(max_length=10)
    phone_number = PhoneNumberField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tx_id}"
