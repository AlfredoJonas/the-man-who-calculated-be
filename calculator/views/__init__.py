import math
from typing import Any
from django.views import View
from wsgiref.simple_server import WSGIRequestHandler
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from calculator import OperationType
from calculator.utils.exceptions import BadRequest
import json
from django.utils.decorators import method_decorator
from calculator.utils.decorators import token_required
from calculator.model_queries import (
    query_filter_to_paginated_api_view,
    query_order_to_paginated_api_view,
    query_search_by_related_conditions,
)
from calculator.utils.random_string import perform_random_string_operation
from calculator.utils.utils import add_success_response, check_keys_on_dict


operation_functions = {
    OperationType.ADDITION.value: lambda A, B: float(A) + float(B),
    OperationType.SUBSTRACTION.value: lambda A, B: float(A) - float(B),
    OperationType.DIVISION.value: lambda A, B: round(float(A) / float(B), 4),
    OperationType.SQUARE_ROOT.value: lambda A: round(math.sqrt(float(A)), 4),
    OperationType.RANDOM_STRING.value: lambda: perform_random_string_operation(),
}


# This code is defining a class-based view in Django that requires authentication using a token.
# This ensures that the view can only be accessed by authenticated users with a valid token.
@method_decorator(token_required, name="dispatch")
class BaseAuthView(View):
    required_fields = []
    model = None

    @staticmethod
    def add_success(response, key="success", status=True):
        return add_success_response(response, key, status)

    def validate_payload(self, payload: dict):
        missing_fields = check_keys_on_dict(self.required_fields, payload)
        if missing_fields:
            raise BadRequest

    def post(self, request: WSGIRequestHandler, **kwargs: Any) -> JsonResponse:
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        if len(self.required_fields) > 0:
            self.validate_payload(body)
        response = self.process_request(request, body)
        return self.add_success(response)

    def get(self, request: WSGIRequestHandler, **kwargs: Any) -> JsonResponse:
        body = request.GET.dict()
        if len(self.required_fields) > 0:
            self.validate_payload(body)
        response = self.process_request(request, body)
        return self.add_success(response)

    def delete(self, request: WSGIRequestHandler, **kwargs: Any) -> JsonResponse:
        body = request.GET.dict()
        if len(self.required_fields) > 0:
            self.validate_payload(body)
        record = self.model.objects.get(id=body.get("id"))
        record.deleted = True
        record.save()
        response = JsonResponse(
            {
                "developer_message": f"The {self.model.__class__.__name__} was deleted",
                "data": {"result": model_to_dict(record)},
            }
        )
        return self.add_success(response)

    def process_request(self, request: WSGIRequestHandler, body: dict):
        raise NotImplemented


class PaginatedView(BaseAuthView):
    allowed_order_filters = []
    search_fields = []
    model = None

    def base_query(self, request):
        # Get all objects from the model
        return self.model.objects.all()

    def process_request(self, request, body):
        # Get query parameters for filtering and ordering
        filter_param = body.get("filter", "")
        order_param = body.get("order", "")
        search = body.get("search", "")
        ordering_conditions = []

        queryset = self.base_query(request)

        # Check if model has deleted field and then use it to filter deleted data
        if hasattr(self.model, "deleted"):
            queryset = queryset.filter(deleted=0)

        # Apply filtering by search fields
        if search and len(self.search_fields) > 0:
            queryset = query_search_by_related_conditions(
                queryset, self.search_fields, search
            )

        # Apply filtering if filter_param is provided
        if filter_param:
            # Split the filters into individual filter conditions
            filter_conditions = filter_param.split(",")
            queryset = query_filter_to_paginated_api_view(
                self.allowed_order_filters, filter_conditions, queryset
            )

        # Apply ordering if order_param is provided
        if order_param:
            # Split the ordering into individual ordering conditions
            ordering_conditions = order_param.split(",")
        elif hasattr(self.model, "created_at"):
            # Check if model has created_at field and then use it to order by default to keep consistency data
            ordering_conditions = ["-created_at"]

        if len(ordering_conditions) > 0:
            queryset = query_order_to_paginated_api_view(
                self.allowed_order_filters, ordering_conditions, queryset
            )

        # Pagination
        page_number = body.get("page", 1)
        size = body.get("size", 10)
        paginator = Paginator(queryset, size)
        try:
            page_obj = paginator.page(page_number)
            data = list(page_obj.object_list.values())
        except Exception:
            # Handle invalid page number gracefully
            data = []

        pagination_data = {
            "total_pages": paginator.num_pages,
            "page": 1,
            "size": 10,
            **body,
        }
        return JsonResponse({"data": data, **pagination_data})


class ApiStatusView(View):
    def get(self, request: WSGIRequestHandler, **kwargs: Any) -> JsonResponse:
        data = {"status": "OK"}
        return JsonResponse(data)
