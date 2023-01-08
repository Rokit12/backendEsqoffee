from django.shortcuts import render
from .models import Feature
from .products.models import ProductCategory, Product


def index(response):
	template = 'index.html'

	features = Feature.objects.all()

	category = None
	categories = ProductCategory.objects.all()
	products = Product.objects.filter(available=True)

	# if category_slug:
	# 	category = get_object_or_404(ProductCategory, slug=category_slug)
	# 	products = products.filter(category=category)

	context = {
		'category': category,
		'categories': categories,
		'products': products,
		'features': features,
	}

	return render(response, template, context)


def about(response):
	template = 'about.html'

	return render(response, template)


def services(response):
	template = 'services.html'
	return render(response, template)
