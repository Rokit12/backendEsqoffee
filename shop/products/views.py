from django.shortcuts import render, get_object_or_404
from shop.cart.forms import CartAddProductForm
from shop.orders.forms import ReservationForm
from .models import ProductCategory, Product
from .recommender import Recommender


def product_list(request, category_slug=None):
    template = 'menu/index.html'

    category = None
    categories = ProductCategory.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(ProductCategory, slug=category_slug)
        products = products.filter(category=category)

    cart_product_form = CartAddProductForm()
    reservation_form = ReservationForm()
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'cart_product_form': cart_product_form,
        'reservation_form': reservation_form,
    }

    return render(request, template, context)


def product_detail(request, id, slug):
    template = 'menu/detail.html'

    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    context = {
        'product': product,
        'recommended_products': recommended_products,
        'cart_product_form': cart_product_form,
    }

    return render(request, template, context)
