from django.shortcuts import render
from .models import Shop, ShopTestimonial
from .products.models import ProductCategory, Product
from .orders.forms import ReservationForm


def index(response):
	template = 'index.html'

	shop = Shop.objects.all()
	shop_testimonials = ShopTestimonial.objects.all()

	category = None
	categories = ProductCategory.objects.all()
	products = Product.objects.filter(available=True)

	reservation_form = ReservationForm()

	context = {
		'category': category,
		'categories': categories,
		'products': products,
		'shop': shop,
		'shop_testimonials': shop_testimonials,
		'reservation_form': reservation_form,
	}

	return render(response, template, context)


def about(response):
	template = 'about.html'
	return render(response, template)


def services(response):
	template = 'services.html'
	return render(response, template)
