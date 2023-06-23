import pytest
import json
from calculator.tests import post_api
from calculator.utils import build_dict_with_required_fields, read_json_file
from calculator.views import operation_functions, required_fields_by_operation

operations_json = read_json_file('fixtures/integrated_operations.json')


def reach_operation(operation, token, variables={"A": 4, "B": 2}):
    req_fields = required_fields_by_operation[operation.type]
    variables = dict(build_dict_with_required_fields(variables, req_fields))
    payload = {
        "operation_id": operation.id,
        "variables": json.dumps(variables)
    }
    headers = {
        'HTTP_AUTHORIZATION': f'Bearer {token}'
    }
    return post_api('/api/newoperation', payload, headers), variables


@pytest.mark.parametrize("operation", operations_json)
def test_success_operations(sample_logged_user_account_token, build_sample_operation, operation):
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
    
    :param sample_logged_user_account_token: It is likely a token that represents a logged-in user
    account. This token is probably used to authenticate the user and authorize them to perform certain
    actions within the system
    :param sample_addition_operation: The `sample_addition_operation` parameter is likely a fixture or a
    sample data object that contains information about an addition operation. It could include details
    such as the type of operation, the variables involved, and any other relevant information needed to
    perform the operation.
    """
    operation = sample_addition_operation[1]
    response, _ = reach_operation(operation, sample_logged_user_account_token.key, {'A': 4})
    data = response.json()
    assert response.status_code == 400
    assert data['developer_message'] == f"Variables field doesn't have the required fields to proccess the operation {operation.type}"
