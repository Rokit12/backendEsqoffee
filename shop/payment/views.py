import logging
import braintree

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from shop.orders.models import Order

from .mpesa import MpesaGateway
from .tasks import payment_completed
from .serializers import MpesaCheckoutSerializer

# instantiate Braintree and MobileMoney payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
gateway_mpesa = MpesaGateway()


@authentication_classes([])
@permission_classes((AllowAny,))
class MpesaCheckout(APIView):
    serializer = MpesaCheckoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.data['phone_number']
            amount = serializer.data['amount']
            reference = serializer.data['reference']
            description = serializer.data['description']

            payload = {
                'request': request,
                'data': {},
                'amount': amount,
                'phone_number': phone_number,
                'account_reference': reference,
                'transaction_description': description,
                'callback_url': f"https://{request.META['HTTP_HOST']}/payment/mpesa/callback"
            }
            res = gateway_mpesa.stk_push_request(payload)
            return Response(res, status=200)


@authentication_classes([])
@permission_classes((AllowAny,))
class MpesaCallBack(APIView):
    def get(self, request):
        return Response({"status": "OK"}, status=200)

    def post(self, request):
        logging.info("Callback from MPESA {}".format(request.body))
        cb = gateway_mpesa.callback_handler(request.body)

        return Response(cb, status=200)


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # launch asynchronous task
            payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
