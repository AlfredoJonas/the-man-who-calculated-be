from django.views import View
from calculator.exceptions import BadRequest
import json
from django.utils.decorators import method_decorator
from calculator.decorators import token_required


# This code is defining a class-based view in Django that requires authentication using a token. 
# This ensures that the view can only be accessed by authenticated users with a valid token.
@method_decorator(token_required, name='dispatch')
class BaseAuthView(View):
    required_fields = []

    def validate_payload(self, payload):
        missing_fields = [field for field in self.required_fields if field not in payload]
        if missing_fields:
            raise BadRequest
    
    def post(self, request, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if len(self.required_fields) > 0:
            self.validate_payload(body)
        return self.process_request(request, body)
        
    def process_request(request, body):
       raise NotImplemented