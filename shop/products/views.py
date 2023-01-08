from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product


def product_list(request, category_slug=None):
    template = 'shop/product/list.html'

    category = None
    categories = ProductCategory.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(ProductCategory, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }

    return render(request, template, context)


def product_detail(request, id, slug):
    template = 'shop/product/detail.html'

    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    context = {
        'product': product
    }

    return render(request, template, context)
