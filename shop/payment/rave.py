import requests
from django.conf import settings

from .models import RaveTransaction


class RaveGateway:

    def __init__(self):
        self.public_key = settings.FLUTTER_PUBLIC_KEY
        self.secret_key = settings.FLUTTER_SECRET_KEY
        self.encryption_key = settings.FLUTTER_ENCRYPTION_KEY

    def checkout_url(self, ref, name, email, amount, phone, callback_url):
        headers = {
            'Authorization': f'Bearer {self.secret_key}'
        }
        data = {
            "tx_ref": ref,
            "amount": amount,
            "currency": "KES",
            "redirect_url": callback_url,
            "payment_options": "card,mpesa",
            "meta": {
                "consumer_id": 23,
                "consumer_mac": "92a3-912ba-1192a"
            },
            "customer": {
                "email": email,
                "phonenumber": phone,
                "name": name
            },
            "customizations": {
                "title": "EsQoffee",
                "description": "Coffee & More",
                "logo": ""
            }
        }

        url = ' https://api.flutterwave.com/v3/payments'
        response = requests.post(url, json=data, headers=headers)
        response = response.json()
        if response['status'] == 'success':
            rave = {
                'tx_reference': ref,
                'amount': amount,
                'phone_number': phone
            }
            RaveTransaction.objects.create(**rave)
            link = response['data']['link']
            return link
        else:
            return None

    def handle_callback(self, txid, ref, status):
        rave = RaveTransaction.objects.get(tx_reference=ref)
        rave.tx_id = txid
        if status == 'successful':
            rave.status = 1
        rave.save()
        return rave
