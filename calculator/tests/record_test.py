from calculator.tests import post_api


def test_addition_operation(sample_logged_user_account_token, sample_addition_operation): 
    payload = {
        "operation_id": sample_addition_operation[1].id,
        "amount": '{"A": 5, "B": 6}'
    }
    headers = {
        'HTTP_AUTHORIZATION': f'Bearer {sample_logged_user_account_token.key}'
    }
    response = post_api('/api/newoperation', payload, headers)
    data = response.json()
    assert response.status_code == 200
    assert data['data']['result'] == 11