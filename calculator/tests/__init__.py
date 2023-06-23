from django.test import Client
import json

def post_api(url, payload={}, headers={}):
    return Client().post(
        url,
        json.dumps(payload),
        'application/json',
        **headers
    )