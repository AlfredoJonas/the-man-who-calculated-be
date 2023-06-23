import pytest
from calculator.models import Operation

@pytest.fixture
@pytest.mark.django_db
def sample_addition_operation(db):
    from calculator.models import User
    operation_payload = {
        "type": "addition",
        "cost": 0.2,
    }
    operation = Operation(**operation_payload)
    operation.save()
    return operation_payload, operation
