from django.contrib import admin
from .models import MpesaTransaction, RaveTransaction

# Register your models here.
admin.site.register(MpesaTransaction)
admin.site.register(RaveTransaction)
