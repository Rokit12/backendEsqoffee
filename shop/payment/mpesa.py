import requests
import logging
import time
import math
import base64

from datetime import datetime
from django.conf import settings
from requests.auth import HTTPBasicAuth
from phonenumber_field.phonenumber import PhoneNumber

from .models import MpesaTransaction

logging = logging.getLogger("default")


class MpesaGateway:
    shortcode = None
    consumer_key = None
    consumer_secret = None
    checkout_url = None
    access_token_url = None
    access_token = None
    access_token_expiration = None
    timestamp = None

    class Decorators:
        @staticmethod
        def refresh_token(decorated):
            def wrapper(gateway, *args, **kwargs):
                if (
                        gateway.access_token_expiration
                        and time.time() > gateway.access_token_expiration
                ):
                    token = gateway.getAccessToken()
                    gateway.access_token = token
                return decorated(gateway, *args, **kwargs)

            return wrapper

    def __init__(self):
        now = datetime.now()
        self.shortcode = settings.MPESA_SHORTCODE
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.access_token_url = settings.MPESA_ACCESS_TOKEN_URL
        self.checkout_url = settings.MPESA_CHECKOUT_URL

        self.password = self.__generate_password()

        try:
            self.access_token = self.get_access_token()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            logging.error("Error {}".format(e))
        else:
            self.access_token_expiration = time.time() + 3400

    def __generate_password(self):
        """Generates mpesa api password using the provided shortcode and passkey"""
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password_str = f'{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{self.timestamp}'
        password_bytes = password_str.encode("ascii")
        return base64.b64encode(password_bytes).decode("utf-8")

    def get_access_token(self):
        try:
            res = requests.get(
                self.access_token_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
            )
        except Exception as err:
            logging.error("Error {}".format(err))
            raise err
        else:
            token = res.json()["access_token"]
            self.headers = {"Authorization": "Bearer %s" % token}
            return token

    @Decorators.refresh_token
    def stk_push_request(self, payload):
        request = payload["request"]
        data = payload["data"]
        amount = payload["amount"]
        account_reference = payload["account_reference"]
        transaction_description = payload["transaction_description"]
        phone_number = payload["phone_number"]
        callback_url = payload["callback_url"]
        req_data = {
            "BusinessShortCode": self.shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(float(amount)),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_description,
        }

        response = requests.post(self.checkout_url, json=req_data, headers=self.headers, timeout=30)
        res_data = response.json()
        logging.info("Mpesa request data {}".format(req_data))
        logging.info("Mpesa response info {}".format(res_data))

        if response.ok:
            data["ip"] = request.META.get("REMOTE_ADDR")
            data["checkout_request_id"] = res_data["CheckoutRequestID"]

            MpesaTransaction.objects.create(**data)
        return res_data

    def callback_handler(self, data):
        print(data)
        try:
            checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
            transaction, _ = MpesaTransaction.objects.get_or_create(
                checkout_request_id=checkout_request_id
            )

            transaction.confirmed = True
            transaction.status = data["Body"]["stkCallback"]["ResultCode"]
            items = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
            for item in items:
                if item["Name"] == "Amount":
                    transaction.amount = item["Value"]
                elif item["Name"] == "MpesaReceiptNumber":
                    transaction.receipt_no = item["Value"]
                elif item["Name"] == "PhoneNumber":
                    transaction.phone_number = PhoneNumber(raw_input=item["Value"])

            transaction.save()
            return transaction
        except Exception as e:
            print(e)
            logging.error(f"Error: {e}")
            return None
