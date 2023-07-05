import pytest


@pytest.fixture
@pytest.mark.django_db
def sample_user_success_account(db):
    from calculator.models import User

    user_payload = {
        "username": "admin@admin.com",
        "password": "admin",
    }
    user = User(**user_payload)
    user.save()
    return user_payload, user


@pytest.fixture
@pytest.mark.django_db
def sample_logged_user_account_token(db, sample_user_success_account):
    from calculator.models import User, Token

    user = User.objects.get(username=sample_user_success_account[1].username)
    token = Token(user=user)
    token.save()
    return token
