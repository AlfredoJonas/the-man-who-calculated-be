from django.db import models
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from datetime import timedelta


class User(models.Model):
    username = models.EmailField(unique=True, help_text='Email to identify the user')
    password = models.CharField(max_length=128, help_text='Encoded password')
    status = models.CharField(max_length=30, default='active', choices=[('ACTIVE', 'active'), ('INACTIVE', 'inactive')], help_text='Let us know if the user was disabled/deleted or it is active')
    last_login = models.DateTimeField(null=True, help_text='Last time the user do login')

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        return super().save(*args, **kwargs)

    def get_email_field_name(self):
        return self.username

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, unique=True, help_text='')
    created_at = models.DateTimeField(auto_now_add=True, help_text='')
    expires_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False, help_text='')

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = default_token_generator.make_token(self.user)
        if not self.expires_at:
            self.expires_at = now() + timedelta(days=1)  # Set token expiration to 1 day from creation
        return super().save(*args, **kwargs)