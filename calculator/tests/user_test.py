import pytest
from calculator.tests import post_api

def reach_login(sample_user_data):
    return post_api('/api/login', sample_user_data)

def test_simple_success_login(sample_user_success_account): 
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
    response = reach_login(payload)
    data = response.json()
    assert response.status_code == status
    assert data['developer_message'] == message


def test_simple_logout(sample_logged_user_account_token):
    headers = {
        'HTTP_AUTHORIZATION': f'Bearer {sample_logged_user_account_token.key}'
    }
    response = post_api('/api/logout', headers=headers)
    data = response.json()
    assert data['developer_message'] == 'Logout successful'
