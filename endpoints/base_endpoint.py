import json
import hashlib
import base64
from ..data.data_api import PAYMENT_API_KEY


class BaseEndpoint:

    @staticmethod
    def generate_signature(data):
        data_json = json.dumps(data, separators=(',', ':')).encode('utf-8')
        encoded_data = base64.b64encode(data_json).decode('utf-8')
        signature_data = encoded_data + PAYMENT_API_KEY
        sign = hashlib.md5(signature_data.encode('utf-8')).hexdigest()
        return sign, data_json
