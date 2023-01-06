from django.shortcuts import render


def index(response):
	return render(response, "home.html")

def about(response):
	return render(response, "about.html")

def contact(response):
	return render(response, "contact.html")

def services(response):
	return render(response, "services.html")
