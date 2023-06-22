from wsgiref.simple_server import WSGIRequestHandler
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View
from calculator.models import User, Token
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime
from calculator.decorators import token_required
import json

# This is a class for handling user login requests and returning a token for authentication.
class LoginView(View):
    def post(self, request: WSGIRequestHandler):
        """
        This function handles user login by checking the validity of the provided credentials and
        returning a token with a lifetime if the login is successful.
        
        :param request: The request parameter is an instance of the WSGIRequestHandler class
        :return: The code returns a JSON response with a message and a token if the login is successful,
        or a JSON response with an error message and a status code of 401 if the login fails.
        """
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body['username']
        try:
            user = User.objects.get(username=username, status='active')
            is_password_valid = check_password(body['password'], user.password)
            if is_password_valid:
                user.last_login = now()
                token, _ = Token.objects.get_or_create(user=user, deleted=False)
                if token.expires_at < datetime.now(timezone.utc):  # Check expiration date
                    token.deleted = True
                    token.save()
                    token, _ = Token.objects.get_or_create(user=user, deleted=False)
                user.save()
                lifetime = (token.expires_at - datetime.now(timezone.utc)).total_seconds()
                return JsonResponse({'message': 'Login successful', 'token': token.key, 'lifetime': lifetime})
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except ObjectDoesNotExist as e:
            return JsonResponse({'message': 'The user doesn\'t exist'}, status=401)


@method_decorator(token_required, name='dispatch')
# This is a class-based view in Python that handles user logout by deleting the user's token.
class LogoutView(View):
    def post(self, request: WSGIRequestHandler):
        """
        This function logs out a user by deleting their token and returns a JSON response indicating
        successful logout.
        
        :param request: The request parameter is an instance of the WSGIRequestHandler class
        :type request: WSGIRequestHandler
        :return: A JSON response with a message indicating that the logout was successful.
        """
        token = Token.objects.get(user=request.user, deleted=False)
        token.deleted = True
        token.save()
        return JsonResponse({'message': 'Logout successful'})
