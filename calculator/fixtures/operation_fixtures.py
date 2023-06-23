import pytest

@pytest.fixture
@pytest.mark.django_db
def sample_addition_operation(db):
    from calculator.models import Operation
    operation_payload = {
        "type": "addition",
        "cost": 0.2,
    }
    operation = Operation(**operation_payload)
    operation.save()
    return operation_payload, operation


@pytest.fixture
@pytest.mark.django_db
def build_sample_operation(db):
    def wrap(type, cost):
        from calculator.models import Operation
        operation_payload = {
            "type": type,
            "cost": cost,
        }
        operation = Operation(**operation_payload)
        operation.save()
        return operation_payload, operation
    return wrap


@pytest.fixture
@pytest.mark.django_db
def sample_addition_record_zero_balance(db, sample_logged_user_account_token, sample_addition_operation):
    from calculator.models import Record
    record_payload = {
        "operation": sample_addition_operation[1],
        "user": sample_logged_user_account_token.user,
        "amount": sample_addition_operation[1].cost,
        "operation_response": "11",
        "user_balance": 0.0
    }
    record = Record(**record_payload)
    record.save()
    return record_payload, record
