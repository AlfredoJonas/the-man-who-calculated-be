from datetime import datetime
from django.contrib.auth.models import User
from django.http import JsonResponse
from calculator.models import Token
from django.utils import timezone

def token_required(view_func):
    def wrapper(request, *args, **kwargs):
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