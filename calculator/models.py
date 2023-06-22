from django.db import models
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from datetime import timedelta


# This is a Django model for a user with email as the username, password encryption, status, and last
# login fields.
class User(models.Model):
    username = models.EmailField(unique=True, help_text='Email to identify the user')
    password = models.CharField(max_length=128, help_text='Encoded password')
    status = models.CharField(max_length=30, default='active', choices=[('ACTIVE', 'active'), ('INACTIVE', 'inactive')], help_text='Let us know if the user was disabled/deleted or it is active')
    last_login = models.DateTimeField(null=True, help_text='Last time the user do login')

    def save(self, *args, **kwargs):
        """
        This function saves a password by encrypting it using the make_password function before calling
        the parent save method.
        :return: The `save()` method of the current object is being called with the arguments `*args`
        and `**kwargs`, and the password attribute of the object is being hashed using the
        `make_password()` function before saving. The `super().save(*args, **kwargs)` method is then
        called to save the object and return the result of the save operation.
        """
        self.password = make_password(self.password)
        return super().save(*args, **kwargs)

    def get_email_field_name(self):
        return self.username

# This is a Django model for a token that belongs to a user and has a unique key, creation and
# expiration dates, and a deleted flag.
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, unique=True, help_text='')
    created_at = models.DateTimeField(auto_now_add=True, help_text='')
    expires_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False, help_text='')

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
            self.expires_at = now() + timedelta(days=1)  # Set token expiration to 1 day from creation
        return super().save(*args, **kwargs)