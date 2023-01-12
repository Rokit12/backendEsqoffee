from django.contrib import admin
from .models import Shop, ShopTestimonial, ShopStory


@admin.register(ShopStory)
class ShopStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'story']


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone', 'email', 'about']


@admin.register(ShopTestimonial)
class ShopTestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'testimony', 'image']

