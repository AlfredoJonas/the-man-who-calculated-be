import math
import random
from django.views import View
from calculator import OperationType
from calculator.exceptions import BadRequest
import json
from django.utils.decorators import method_decorator
from calculator.decorators import token_required
from calculator.utils import check_keys_on_dict

operation_functions = {
    OperationType.ADDITION.value: lambda A, B: float(A) + float(B),
    OperationType.SUBSTRACTION.value: lambda A, B: float(A) - float(B),
    OperationType.DIVISION.value: lambda A, B: float(A) / float(B),
    OperationType.SQUARE_ROOT.value: lambda A: math.sqrt(A),
    OperationType.RANDOM_STRING.value:  lambda: "RANDOM STR"
}

required_fields_by_operation = {
    OperationType.ADDITION.value: ['A', 'B'],
    OperationType.SUBSTRACTION.value: ['A', 'B'],
    OperationType.DIVISION.value: ['A', 'B'],
    OperationType.SQUARE_ROOT.value: ['A'],
    OperationType.RANDOM_STRING.value:  []
}

# This code is defining a class-based view in Django that requires authentication using a token. 
# This ensures that the view can only be accessed by authenticated users with a valid token.
@method_decorator(token_required, name='dispatch')
class BaseAuthView(View):
    required_fields = []

    def validate_payload(self, payload):
        missing_fields = check_keys_on_dict(self.required_fields, payload)
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