import weasyprint

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from shop.cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm, ReservationForm
from .tasks import order_created


def book_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return redirect(reverse('home'))


def order_process(request):
    template = 'orders/create.html'

    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                item_product = item['product']
                item_price = item['price']
                item_quantity = item['quantity']

                OrderItem.objects.create(order=order, product=item_product, price=item_price, quantity=item_quantity)

            # clear the cart
            cart.clear()

            # launch asynchronous task
            order_created.delay(order.id)

            # set the order in the session
            request.session['order_id'] = order.id

            payment_option = order.payment_option
            if payment_option == 'cash':
                return redirect(reverse('home'))
            else:
                return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()

    return render(request, template, {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html', {'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint \
        .HTML(string=html) \
        .write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')])

    return response
