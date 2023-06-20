from datetime import datetime
from django.contrib.auth.models import User
from django.http import JsonResponse
from calculator.models import Token

def token_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth_header = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth_header) == 2 and auth_header[0].lower() == 'token':
                token = auth_header[1]
                try:
                    token_obj = Token.objects.get(key=token)
                    if token_obj.expires_at >= datetime.now():  # Check expiration date
                        request.user = token_obj.user
                        return view_func(request, *args, **kwargs)
                    else:
                        return JsonResponse({'message': 'Expired token, please refresh with /login endpoint'}, status=401)
                except Token.DoesNotExist:
                    pass
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    return wrapper