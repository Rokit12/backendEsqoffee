from django.shortcuts import render
from .models import Feature


def index(response):
	template = 'home.html'

	features = Feature.objects.all()
	context = {
		'features': features,
	}
	return render(response, template, context)


def about(response):
	template = 'about.html'

	return render(response, template)


def services(response):
	template = 'services.html'
	return render(response, template)
