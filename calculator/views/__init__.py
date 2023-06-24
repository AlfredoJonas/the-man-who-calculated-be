import math
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from calculator import OperationType
from calculator.exceptions import BadRequest
import json
from django.utils.decorators import method_decorator
from calculator.decorators import token_required
from calculator.model_queries import apply_filter_to_paginated_api_view, apply_order_to_paginated_api_view
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
    
    
    def get(self, request, **kwargs):
        body = request.GET.dict()
        if len(self.required_fields) > 0:
            self.validate_payload(body)
        return self.process_request(request, body)
        
    def process_request(request, body):
       raise NotImplemented

class PaginatedView(BaseAuthView):
    allowed_filters = []
    model = None
    def process_request(self, request, body):
        # Get query parameters for filtering and ordering
        filter_param = body.get('filter', '')
        order_param = body.get('order', '')

        # Get all objects from the model
        queryset = self.model.objects.all()

        # Apply filtering if filter_param is provided
        if filter_param:
            # Split the filters into individual filter conditions
            filter_conditions = filter_param.split(',')
            queryset = apply_filter_to_paginated_api_view(self.allowed_filters, filter_conditions, queryset)

        # Apply ordering if order_param is provided
        if order_param:
            # Split the ordering into individual ordering conditions
            ordering_conditions = order_param.split(',')
            queryset = apply_order_to_paginated_api_view(ordering_conditions, queryset)

        # Pagination
        page_number = body.get('page', 1)
        size = body.get('size', 10)
        paginator = Paginator(queryset, str(size))  # Show 10 objects per page
        try:
            page_obj = paginator.page(page_number)
            data = list(page_obj.object_list.values())
        except Exception:
            # Handle invalid page number gracefully
            data = []
        
        return JsonResponse({'data': data, **body})
    