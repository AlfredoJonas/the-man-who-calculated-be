from django.db import models
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from datetime import timedelta
from calculator import UserStatus, OperationType, USER_STATUSES, OPERATION_TYPES


class User(models.Model):
    username = models.EmailField(unique=True, help_text="Email to identify the user")
    password = models.CharField(max_length=128, help_text="Encoded password")
    status = models.CharField(
        max_length=30,
        default=UserStatus.ACTIVE.value,
        choices=USER_STATUSES,
        help_text="Let us know if the user was disabled/deleted or it is active",
    )
    last_login = models.DateTimeField(
        null=True, help_text="Last time the user do login"
    )
    balance = models.FloatField(
        default=5, help_text="How much left to the user to process new operations"
    )

    def save(self, *args, **kwargs):
        """
        This function saves a password by encrypting it using the make_password function before calling
        the parent save method.
        :return: The `save()` method of the current object is being called with the arguments `*args`
        and `**kwargs`, and the password attribute of the object is being hashed using the
        `make_password()` function before saving. The `super().save(*args, **kwargs)` method is then
        called to save the object and return the result of the save operation.
        """
        is_new_record = not bool(self.pk)
        if is_new_record:
            self.password = make_password(self.password)
        self.balance = round(self.balance, 2)  # Round the number
        return super().save(*args, **kwargs)

    def get_email_field_name(self):
        return self.username


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(
        max_length=64,
        unique=True,
        help_text="token generated by auth.tokens library using the secret key stored on settings.py",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date the token was created"
    )
    expires_at = models.DateTimeField(
        null=True, help_text="Datetime the token will expire"
    )
    deleted = models.BooleanField(default=False, help_text="For logical deletion")

    def save(self, *args, **kwargs):
        """
        This function saves a token with a default expiration time of 1 day if no expiration time is
        provided.
        :return: The return value of the `save()` method is the return value of the `save()` method of
        the parent class (`super().save(*args, **kwargs)`).
        """
        if not self.key:
            self.key = default_token_generator.make_token(self.user)
        if not self.expires_at:
            self.expires_at = now() + timedelta(
                days=1
            )  # Set token expiration to 1 day from creation
        return super().save(*args, **kwargs)


class Operation(models.Model):
    type = models.CharField(
        max_length=30,
        default=OperationType.ADDITION.value,
        choices=OPERATION_TYPES,
        help_text="Let us know if the user was disabled/deleted or it is active",
    )
    cost = models.FloatField(
        default=0, help_text="How much the type of operation cost to the user"
    )
    fields = models.JSONField(
        default=dict, help_text="Store required fields to perform the operation"
    )


class Record(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, help_text="How much cost the operation")
    user_balance = models.FloatField(
        default=5, help_text="How much left to the user to process new operations"
    )
    operation_response = models.CharField(
        max_length=120,
        default="",
        help_text="The result of the operation calculated, it could be a number or a random string",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date the record was created"
    )
    deleted = models.BooleanField(default=False, help_text="For logical deletion")

    def save(self, *args, **kwargs):
        self.user_balance = round(self.user_balance, 2)  # Round the number
        super().save(*args, **kwargs)
