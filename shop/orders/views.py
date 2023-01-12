import weasyprint
import decimal

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from django_daraja.mpesa.core import MpesaClient

from shop.cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created

# instantiate MobileMoney payment gateway
gateway_mpesa = MpesaClient()


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
            if payment_option == 'card':
                # redirect for payment
                return redirect(reverse('payment:process'))
            elif payment_option == 'mpesa':
                amount = int(order.get_total_cost())
                account_reference = order.id

                phone_number = order.phone
                if phone_number[0] == "+":
                    phone_number = phone_number[1:]
                elif phone_number[0] == "0":
                    phone_number = "254" + phone_number[1:]

                gateway_mpesa.access_token()
                a = gateway_mpesa.stk_push(
                    phone_number,
                    amount,
                    account_reference,
                    order.id,
                    f"https://{request.META['HTTP_HOST']}/payment/mpesa/callback"
                )
                print(a.error_message)

                return redirect(reverse('payment:done'))
            else:
                return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()

    return render(request, template, {'cart': cart, 'form': form})


def order_create(request):
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
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()

    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, template, context)


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
