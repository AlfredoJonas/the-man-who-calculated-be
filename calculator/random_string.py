import os
import requests


def perform_random_string_operation():
    random_str_payload = {
        "jsonrpc": "2.0",
        "method": "generateStrings",
        "params": {
            "apiKey": f"{os.environ.get('RANDOM_API_KEY')}",
            "n": 1,
            "length": 10,
            "characters": "abcdefghijklmnopqrstuvwxyz",
            "replacement": True
        },
        "id": 42
    }
    response = requests.post(
                    os.environ.get('RANDOM_V4_API_URL'),
                    data=random_str_payload,
                )
    
    return response.get('result', {}).get('random', {}).get('data', [''])[0]