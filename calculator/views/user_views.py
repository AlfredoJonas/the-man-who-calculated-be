from wsgiref.simple_server import WSGIRequestHandler
from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View
from calculator import UserStatus
from calculator.utils.exceptions import BadRequest, Unauthorized, NotFound
from calculator.models import User, Token
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime
import json
from calculator.utils.utils import check_keys_on_dict
from calculator.views import BaseAuthView

# This is a class for handling user login requests and returning a token for authentication.
class LoginView(View):
    required_fields = ['username', 'password']

    def validate_payload(self, payload: dict):
        missing_fields = check_keys_on_dict(self.required_fields, payload)
        if missing_fields:
            raise BadRequest
    
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
        self.validate_payload(body)
        username = body['username']
        try:
            user = User.objects.get(username=username, status=UserStatus.ACTIVE.value)
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
                response = JsonResponse(
                    {
                        'developer_message': 'Login successful',
                        'lifetime': lifetime,
                        'data': {"username": user.username, "balance": user.balance}
                    })
                
                # Set the cookie with SameSite=None and Secure attributes
                response.set_cookie('auth_token', token.key, samesite='None', secure=False, httponly=True)
                response.set_cookie('Access-Control-Allow-Credentials', True, samesite='None',  secure=False, httponly=True)
                response.set_cookie('Access-Control-Allow-Origin', "*", samesite='None',  secure=False, httponly=True)

                return response
            else:
                raise Unauthorized('Invalid credentials')
        except ObjectDoesNotExist as e:
            raise NotFound('The user doesn\'t exist')


# This is a class-based view in Python that handles user logout by deleting the user's token.
class LogoutView(BaseAuthView):
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
        return JsonResponse({'developer_message': 'Logout successful'})


# This is a class-based view in Python that handles user logout by deleting the user's token.
class UserView(BaseAuthView):
    def process_request(self, request: WSGIRequestHandler, body, *args, **kwargs):
        return JsonResponse({'data': {"username": request.user.username, "user_balance": round(request.user.balance,2)}})
