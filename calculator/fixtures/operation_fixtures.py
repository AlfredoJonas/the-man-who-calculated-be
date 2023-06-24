import pytest
import random
from calculator import OperationType


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


@pytest.fixture
@pytest.mark.django_db
def sample_operation_records(db):
    from calculator.models import Operation
    from calculator.utils import read_json_file
    
    operations_json = read_json_file('fixtures/integrated_operations.json')

    operations = []
    for operation_dict in operations_json:
        operation = Operation(**operation_dict['fields'])
        operation.save()
        operations.append(operation)

    return operations


@pytest.fixture
@pytest.mark.django_db
def build_sample_records(db, sample_logged_user_account_token, sample_operation_records):
    def wrap(amount):
        from calculator.models import Record
        records = {
            OperationType.ADDITION.value: [],
            OperationType.SUBSTRACTION.value: [],
            OperationType.DIVISION.value: [],
            OperationType.SQUARE_ROOT.value: [],
            OperationType.RANDOM_STRING.value: [],
        }
        for _ in range(amount):
            operation = random.choice(sample_operation_records)
            record_payload = {
                "operation": operation,
                "user": sample_logged_user_account_token.user,
                "amount": operation.cost,
                "operation_response": str(random.randint(10,1000)),
                "user_balance": round(random.uniform(0, 5),2)
            }
            record = Record(**record_payload)
            record.save()
            records[operation.type].append(record)
        return records
    return wrap

@pytest.fixture
def random_string_mock_response(monkeypatch):
    random_string =str(random.randint(1000,10000))
    def fake_post_event(path, **kwargs):
        return {
            "jsonrpc": "2.0",
            "result": {
                "random": {
                    "data": [
                        random_string
                    ],
                    "completionTime": "2023-06-24 04:24:26Z"
                },
                "bitsUsed": 47,
                "bitsLeft": 249906,
                "requestsLeft": 998,
                "advisoryDelay": 1610
            },
            "id": 42
        }

    monkeypatch.setattr("requests.post", fake_post_event)
