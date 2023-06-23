import pytest
from calculator.tests import post_api

def reach_login(sample_user_data):
    return post_api('/api/login', sample_user_data)

def test_simple_success_login(sample_user_success_account): 
    """
    This function tests a simple successful login by sending a request to the login endpoint and
    checking if the response status code is 200 and the developer message is "Login successful".
    
    :param sample_user_success_account: It is a fixture that returns a sample user
    account that has valid login credentials. The fixture return a tuple or a list
    containing the username and password of the sample user account
    """
    response = reach_login(sample_user_success_account[0])
    data = response.json()
    assert response.status_code == 200
    assert data['developer_message'] == 'Login successful'

@pytest.mark.parametrize(
    "payload, message, status",
    [
        (
            {
                "username": "wrong@username.email",
                "password": "wrong password",
            },
            'The user doesn\'t exist',
            404
        ),
        (
            {
                "username": "admin@admin.com",
                "password": "wrong password",
            },
            'Invalid credentials',
            401
        ),
    ],
)
def test_simple_error_login(sample_user_success_account, payload, message, status):
    """
    This is a pytest function that tests for error messages and status codes when attempting to log in
    with incorrect credentials.
    
    :param sample_user_success_account: It is a fixture that sets up a sample user account with
    valid credentials for testing purposes
    :param payload: A dictionary containing the username and password for the login attempt
    :param message: The error message that is expected to be returned by the API in case of a failed
    login attempt
    :param status: The expected HTTP status code of the response
    """
    response = reach_login(payload)
    data = response.json()
    assert response.status_code == status
    assert data['developer_message'] == message


def test_simple_logout(sample_logged_user_account_token):
    """
    This function tests if a user can successfully log out of their account.
    
    :param sample_logged_user_account_token: It is a token that represents a logged-in user account.
    This token is used to authenticate the user when making requests to the API. The token is passed in
    the HTTP Authorization header as a Bearer token
    """
    headers = {
        'HTTP_AUTHORIZATION': f'Bearer {sample_logged_user_account_token.key}'
    }
    response = post_api('/api/logout', headers=headers)
    data = response.json()
    assert data['developer_message'] == 'Logout successful'
