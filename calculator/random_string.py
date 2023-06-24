import os
import requests


def perform_random_string_operation():
    """
    The function generates a random string using an API call and returns the generated string.
    :return: a randomly generated string of length 10, consisting of lowercase alphabets, obtained from
    an API call using the `requests` library. The API key and URL are obtained from environment
    variables.
    """
    random_str_payload = {
        "jsonrpc": "2.0",
        "method": "generateStrings",
        "params": {
            "apiKey": os.environ.get("RANDOM_API_KEY"),
            "n": 1,
            "length": 10,
            "characters": "abcdefghijklmnopqrstuvwxyz",
            "replacement": True
        },
        "id": 42
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
                    os.environ.get("RANDOM_V4_API_URL"),
                    json=random_str_payload,
                    headers=headers
                )
    data = response.json()
    return data.get('result', {}).get('random', {}).get('data', [''])[0]