from django.shortcuts import render, redirect, get_object_or_404
from shop.orders.models import Order

from .tasks import payment_completed
from .rave import RaveGateway

gateway = RaveGateway()


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    link = gateway.checkout_url(
        order_id,
        f'{order.first_name} {order.last_name}',
        order.email,
        total_cost,
        order.phone,
        f"{request.scheme}://{request.META['HTTP_HOST']}/payment/done"
    )
    if link is not None:
        return redirect(link)
    else:
        return redirect('payment:canceled')


def payment_done(request):
    transaction_id = request.GET.get('transaction_id', None)
    tx_ref = request.GET.get('tx_ref', None)
    status = request.GET.get('status', None)

    if status == 'successful':
        order = Order.objects.get(id=tx_ref)
        order.transaction_id = transaction_id
        order.paid = True
        order.save()
        payment_completed.delay(order.id)

    gateway.handle_callback(transaction_id, tx_ref, status)
    return redirect('menu:product_list')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
