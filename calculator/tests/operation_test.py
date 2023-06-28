import math
import pytest
import json
from calculator import OperationType
from calculator.tests import get_api, post_api, delete_api
from calculator.utils.utils import build_dict_with_required_fields, read_json_file
from calculator.views import operation_functions

operations_json = read_json_file('calculator/fixtures/integrated_operations.json')


def reach_operation(operation, token, variables={"A": 4, "B": 2}):
    req_fields = list(operation.fields.keys())
    variables = dict(build_dict_with_required_fields(variables, req_fields))
    payload = {
        "operation_id": operation.id,
        "variables": json.dumps(variables)
    }
    return post_api('/api/record', payload, token), variables


def get_operation(token, page: int = 1, size: int = 10, filter: str = "", order: str = ""):
    payload = {
        "page": page,
        "size": size,
        "filter": filter,
        "order": order
    }
    return get_api('/api/operations', payload, token)


def get_records(token, page: int = 1, size: int = 10, search: str = "", filter: str = "", order: str = ""):
    payload = {
        "page": page,
        "size": size,
        "search": search,
        "filter": filter,
        "order": order
    }
    return get_api('/api/records', payload, token)


@pytest.mark.parametrize("operation", operations_json)
def test_success_operations(sample_logged_user_account_token, build_sample_operation, operation, random_string_mock_response):
    """
    This is a pytest function that tests the success of various operations using parameters from a JSON
    file.
    
    :param sample_logged_user_account_token: `sample_logged_user_account_token` is a
    fixture that provides a token for a logged-in user account. This token is likely used to
    authenticate the user and allow them to perform certain actions in the test
    :param build_sample_operation: `build_sample_operation` is a fixture function that takes in fields as
    arguments and returns a tuple containing an `Operation` object and a dictionary of variables to be
    used in the operation
    :param operation: "operation" is a parameterized input for a test function. It is being passed
    values from the "operations_json" list for each test run. The test function is testing the success
    of various operations by building a sample operation using the "build_sample_operation" function
    """
    _, operation = build_sample_operation(**operation['fields'])
    response, variables = reach_operation(operation, sample_logged_user_account_token.key)
    data = response.json()
    assert response.status_code == 200
    operation_function = operation_functions[operation.type]
    result = operation_function(**variables)
    assert data['data']['result'] == result


def test_addition_operation_out_of_money(sample_logged_user_account_token, sample_addition_record_zero_balance): 
    """
    This function tests if an addition operation can be performed when the user's balance is zero.
    
    :param sample_logged_user_account_token: It is a token that represents a logged-in user account.
    This token is used to authenticate the user and authorize their actions
    :param sample_addition_record_zero_balance: It seems like `sample_addition_record_zero_balance` is a
    tuple containing two elements. The first element is not shown in the code snippet, but the second
    element is an object with attributes `operation` and `user_balance`. The `operation` attribute is an
    object with a `type` attribute
    """
    operation = sample_addition_record_zero_balance[1].operation
    user_balance = sample_addition_record_zero_balance[1].user_balance
    response, _ = reach_operation(operation, sample_logged_user_account_token.key)
    data = response.json()
    assert response.status_code == 402
    assert data['developer_message'] == f'User balance({user_balance}) is not enough to perform an operation({operation.type}) of {operation.cost}'


def test_invalid_addition_operation_payload(sample_logged_user_account_token, sample_addition_operation): 
    """
    The function tests for an invalid addition operation payload and checks if the response status code
    is 400 and the developer message is correct.
    
    :param sample_logged_user_account_token: It is a token that represents a logged-in user
    account. This token is probably used to authenticate the user and authorize them to perform certain
    actions within the system
    :param sample_addition_operation: The `sample_addition_operation` parameter is a fixture or a
    sample data object that contains information about an addition operation. It could include details
    such as the type of operation, the variables involved, and any other relevant information needed to
    perform the operation.
    """
    operation = sample_addition_operation[1]
    response, _ = reach_operation(operation, sample_logged_user_account_token.key, {'A': 4})
    data = response.json()
    assert response.status_code == 400
    assert data['developer_message'] == f"Variables field doesn't have the required fields to proccess the operation {operation.type}"

def test_get_operations(sample_logged_user_account_token, sample_operation_records):
    """
    The function tests the functionality of retrieving operations data from an API endpoint.
    
    :param sample_logged_user_account_token: This is a token that represents a logged-in user
    account. It is used to authenticate the user and ensure that they have the necessary permissions to
    access the API endpoint being tested
    :param sample_operation_records: It is a fixture that contains
    operation records. These records are likely used for testing the functionality of the
    "get_operations" API endpoint
    """
    response =  get_operation(sample_logged_user_account_token.key)
    data = response.json()
    assert response.status_code == 200
    assert len(data['data']) >= 5


def test_get_filtered_operations_v1(sample_logged_user_account_token, sample_operation_records):
    """
    This function tests the functionality of filtering operations by type using a sample user account
    token and operation records.
    
    :param sample_logged_user_account_token: This is a token that represents a logged-in user account.
    It is used to authenticate the user and authorize access to certain resources or actions within the
    system
    :param sample_operation_records: It is a fixture or a function that generates sample
    operation records for testing purposes.
    """
    filter = f"type:{OperationType.ADDITION.value}"
    response =  get_operation(sample_logged_user_account_token.key, filter=filter)
    data = response.json()
    assert response.status_code == 200
    assert len(data['data']) >= 1


def test_get_filtered_operations_v2(sample_logged_user_account_token, sample_operation_records):
    """
    This function tests the functionality of filtering operations based on cost greater than a certain
    value.
    
    :param sample_logged_user_account_token: This is a token that represents a logged-in user account.
    It is likely used to authenticate the user and ensure that they have the necessary permissions to
    access the API endpoint being tested
    :param sample_operation_records: It is a fixture that provides a list of sample operation records
    for testing purposes
    """
    filter = f"cost__gt:0.03"
    response =  get_operation(sample_logged_user_account_token.key, filter=filter)
    data = response.json()
    assert response.status_code == 200
    assert len(data['data']) >= 3


def test_get_filtered_records_v1(sample_logged_user_account_token, build_sample_records):
    """
    This function tests the functionality of filtering and paginating records in an API endpoint.
    
    :param sample_logged_user_account_token: This is a sample authentication token for a logged-in user
    account. It is likely used to authenticate the user making the API request to retrieve filtered
    records
    :param build_sample_records: It is a function that builds a list of sample records for testing
    purposes. The function takes an integer argument that specifies the number of records to generate
    """
    build_sample_records(15)
    response =  get_records(sample_logged_user_account_token.key)
    data = response.json()
    assert response.status_code == 200
    assert len(data['data']) == 10


def test_get_filtered_records_v2(sample_logged_user_account_token, build_sample_records):
    """
    This function tests the functionality of filtering records by operation type and checks if the total
    pages returned are correct.
    
    :param sample_logged_user_account_token: It is a token that represents a logged-in user account.
    This token is used to authenticate the user and authorize access to certain resources or actions
    within the system
    :param build_sample_records: A function that builds a list of sample records for testing purposes
    """
    records = build_sample_records(100)
    filter = f"operation__type:{OperationType.SUBSTRACTION.value}"
    response =  get_records(sample_logged_user_account_token.key, filter=filter)
    data = response.json()
    assert response.status_code == 200
    assert data['total_pages'] == math.ceil(len(records[OperationType.SUBSTRACTION.value])/10)


def test_get_filtered_records_v3(sample_logged_user_account_token, build_sample_records):
    """
    This function tests the functionality of getting filtered records based on a search query.
    
    :param sample_logged_user_account_token: It is a token that represents a logged-in user account.
    This token is used to authenticate the user and authorize access to certain resources or actions
    within the system
    :param build_sample_records: It is a function that builds a sample set of records for testing
    purposes. The function takes two arguments: the number of records to create and the type of records
    to create (in this case, 'addition'). It returns a dictionary of records
    """
    records = build_sample_records(5, 'addition')['addition']
    search = "admin"
    response =  get_records(sample_logged_user_account_token.key, search=search)
    data = response.json()
    assert response.status_code == 200
    assert len(data['data']) == 5 == len(records)


def test_get_filtered_records_v4(sample_logged_user_account_token, build_sample_records):
    build_sample_records(5, 'addition')['addition']
    search = "random"
    response =  get_records(sample_logged_user_account_token.key, search=search)
    data = response.json()
    assert response.status_code == 200
    assert len(data['data']) == 0

def test_delete_record(sample_logged_user_account_token, build_sample_records):
    record = build_sample_records(1, 'addition')['addition'][0]
    response = delete_api(f'/api/record/delete?id={record.id}', token=sample_logged_user_account_token.key)
    data = response.json()
    assert response.status_code == 200
    assert data['data']['result']['id'] == record.id
    assert data['data']['result']['deleted'] == 1
