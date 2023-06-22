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

class LoginView(View):
    def post(self, request):
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
class LogoutView(View):
    def post(self, request):
        token = Token.objects.get(user=request.user, deleted=False)
        token.deleted = True
        token.save()
        return JsonResponse({'message': 'Logout successful'})
