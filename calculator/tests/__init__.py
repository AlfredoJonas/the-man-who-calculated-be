from django.test import Client
import json

def post_api(url: str, payload:dict = {}, headers:dict = {}):
    return Client().post(
        url,
        json.dumps(payload),
        'application/json',
        **headers
    )

def get_api(url: str, payload:dict = {}, headers:dict = {}):
    return Client().get(
        url,
        payload,
        content_type='application/json',
        **headers
    )
    