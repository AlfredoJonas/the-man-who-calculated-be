from django.test import Client
import json

def post_api(url: str, payload:dict = {}, token = '', headers:dict = {}):
    client = Client()
    client.cookies['auth_token'] = token
    client.cookies['auth_token']['httponly'] = True
    return client.post(
        url,
        json.dumps(payload),
        'application/json',
        **headers
    )

def get_api(url: str, payload:dict = {}, token = '', headers:dict = {}):
    client = Client()
    client.cookies['auth_token'] = token
    client.cookies['auth_token']['httponly'] = True
    return client.get(
        url,
        payload,
        content_type='application/json',
        **headers
    )
    

def delete_api(url: str, payload:dict = {}, token = '', headers:dict = {}):
    client = Client()
    client.cookies['auth_token'] = token
    client.cookies['auth_token']['httponly'] = True
    return client.delete(
        url,
        payload,
        content_type='application/json',
        **headers
    )
    