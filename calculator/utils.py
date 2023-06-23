import os
import json

def read_json_file(url):
    """
    This function reads a JSON file from a given URL and returns its contents as a Python object.
    
    :param url: The `url` parameter is a string that represents the path to a JSON file. It is used to
    locate and read the JSON file
    :return: The function `read_json_file` returns the data loaded from a JSON file located at the
    specified URL.
    """
    file_path = os.path.join(os.path.dirname(__file__), url)
    
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    
    return data

def check_keys_on_dict(keys, dictionary):
    """
    The function checks if all the keys in a list are present in a dictionary and returns a list of
    missing keys.
    
    :param keys: A list of strings representing the keys that should be present in the dictionary
    :param dictionary: A Python dictionary that contains key-value pairs
    :return: The function `check_keys_on_dict` takes in two arguments: `keys` and `dictionary`. It
    returns a list of all the keys in `keys` that are not present in `dictionary`.
    """
    return [field for field in keys if field not in dictionary]

def build_dict_with_required_fields(variables, req_fields):
    """
    This function builds a dictionary with only the required fields from a given dictionary.
    
    :param variables: The variables parameter is a dictionary containing key-value pairs of variables
    :param req_fields: The `req_fields` parameter is a list of strings representing the required fields
    that should be present in the `variables` dictionary. The function will only include the key-value
    pairs in the returned dictionary if the key is present in the `req_fields` list
    :return: a dictionary containing only the key-value pairs from the input `variables` dictionary that
    have keys that match the required fields specified in the `req_fields` list. If a key in
    `req_fields` is not present in `variables`, it will not be included in the returned dictionary.
    """
    variables = {req_field: variables[req_field] for req_field in req_fields if req_field in variables}
    return variables
