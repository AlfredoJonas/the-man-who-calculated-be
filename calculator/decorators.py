from datetime import datetime
from wsgiref.simple_server import WSGIRequestHandler
from django.contrib.auth.models import User
from django.http import JsonResponse
from calculator.models import Token
from django.utils import timezone

def token_required(view_func):
    """
    This is a decorator function that checks if a token is valid and not expired before allowing access
    to a view function.
    
    :param view_func: The view function that is being decorated by the token_required decorator
    :return: A decorated function that checks for a valid token in the request header and sets the
    request user if the token is valid. If the token is invalid or expired, it returns a JSON response
    with an appropriate error message and status code.
    """
    def wrapper(request: WSGIRequestHandler, *args: dict, **kwargs: dict):
        try:
            auth_header = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth_header) == 2 and auth_header[0].lower() == 'bearer':
                token = auth_header[1]
                token_obj = Token.objects.get(key=token, deleted=False)
                if token_obj.expires_at >= datetime.now(timezone.utc):  # Check expiration date
                    request.user = token_obj.user
                    return view_func(request, *args, **kwargs)
                else:
                    return JsonResponse({'message': 'Expired token, please refresh with /login endpoint'}, status=401)
        except Exception:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return wrapper