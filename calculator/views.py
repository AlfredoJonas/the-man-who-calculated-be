from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views import View
from calculator.models import User, Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime
import json

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body['username']
        user = User.objects.get(username=username, status='active')
        is_password_valid = check_password(body['password'], user.password)
        if user and is_password_valid:
            user.last_login = now()
            token, _ = Token.objects.get_or_create(user=user, deleted=False)
            if token.expires_at < datetime.now(timezone.utc):  # Check expiration date
                token.deleted = True
                token.save()
                token, _ = Token.objects.get_or_create(user=user, deleted=False)
            user.save()
            lifetime = (token.expires_at - datetime.now(timezone.utc)).total_seconds()
            return JsonResponse({'message': 'Login successful', 'token': token.key, 'lifetime': lifetime})
        return JsonResponse({'message': 'Invalid credentials'}, status=401)

class LogoutView(View):
    def post(self, request):
        return JsonResponse({'message': 'Logout successful'})
