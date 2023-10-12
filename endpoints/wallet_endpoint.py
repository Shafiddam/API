import json

import requests
from .base_endpoint import BaseEndpoint
from ..data.data_api import ID_MERCHANT


class WalletEndpoint(BaseEndpoint):
    BASE_URL = 'https://api.cryptomus.com/v1/wallet'

    @classmethod
    def create_wallet(cls, data):
        sign, data_json = cls.generate_signature(data)
        headers = {
            'Content-Type': 'application/json',
            'merchant': ID_MERCHANT,
            'sign': sign
        }
        response = requests.post(cls.BASE_URL, headers=headers, data=data_json)
        return response, sign

    @classmethod
    def block_address(cls, data):
        sign, data_json = cls.generate_signature(data)
        headers = {
            'Content-Type': 'application/json',
            'merchant': ID_MERCHANT,
            'sign': sign
        }
        response = requests.post(f"{cls.BASE_URL}/block-address", headers=headers, data=data_json)
        return response, sign