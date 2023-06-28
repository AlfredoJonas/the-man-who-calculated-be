from wsgiref.simple_server import WSGIRequestHandler
from django.http import JsonResponse
import json
from django.core.exceptions import ObjectDoesNotExist
from calculator import BASE_USER_BALANCE
from calculator.utils.exceptions import BadRequest, NotFound, OutOfMoney
from calculator.models import Operation, Record, User
from calculator.utils.utils import add_success_response, check_keys_on_dict
from calculator.views import BaseAuthView, PaginatedView
from calculator.views import operation_functions


class NewOperationView(BaseAuthView):
    """
    The NewOperationView class is a view that processes requests for performing multiple operations and
    checks if the user has enough balance to perform the operation.
    """
    required_fields = ['operation_id', 'variables']

    @staticmethod
    def check_variable_payload(variables, operation):
        """
        The function checks if a dictionary of variables has the required fields for a given operation
        type and raises an exception if not.
        
        :param variables: A dictionary containing the variables needed to process a specific operation
        :param operation_type: The type of operation being performed. It is used to determine which
        fields are required in the "variables" parameter
        """
        required_keys = operation.fields.keys()
        if check_keys_on_dict(required_keys, variables):
            raise BadRequest(f"Variables field doesn't have the required fields to proccess the operation {operation.type}")
        elif  len(required_keys) < len(list(variables.keys())):
            raise BadRequest(f"Variables field has more fields than expected to proccess the operation {operation.type}")


    @staticmethod
    def get_variables(variables):
        """
        This is a static method in Python that takes a string of variables, converts it to a dictionary
        using JSON, and returns an empty dictionary if no variables are provided.
        
        :param variables: The "variables" parameter is a string that represents a JSON object containing
        variables. If the string is empty or None, an empty dictionary is returned. If the string cannot
        be parsed as JSON, an empty dictionary is also returned
        :return: The `get_variables` method returns a dictionary object. If the `variables` parameter is
        not `None`, it is converted from a JSON string to a dictionary object using the `json.loads()`
        method. If the conversion fails, an empty dictionary is returned. If `variables` is `None` or an
        empty string, an empty dictionary is returned.
        """
        try:
            variables = variables if variables else "{}"
            variables = json.loads(variables)
        except:
            variables = {}
        if not variables:
            variables = {}
        return variables
        
    @staticmethod
    def check_balance(user: User, operation: Operation):
        """
        This function checks the balance of a user after a given operation.
        
        :param user: The user object represents the user for whom we want to check the balance
        :type user: User
        :param operation: The `operation` parameter is an instance of the `Operation` model class, which
        represents a transaction or operation that a user can perform in the system. It has a `cost`
        attribute that represents the amount of money that the operation costs
        :type operation: Operation
        :return: The `check_balance` method returns a tuple containing the user's current balance
        (either the last recorded balance or the base user balance if there are no records) and the new
        balance after deducting the cost of the operation.
        """
        new_user_balance = user.balance - operation.cost
        return user.balance, new_user_balance

    def process_request(self, request: WSGIRequestHandler, body: json):
        """
        This function processes a request by performing an addition operation and saving the result in a
        record if the user has enough balance.
        
        :param request: The `request` parameter is an instance of the `WSGIRequestHandler` class, which
        represents the HTTP request made to the server. It contains information such as the request
        method, headers, and query parameters
        :type request: WSGIRequestHandler
        :param body: The `body` parameter is a JSON object that contains the request body data sent to
        the server. It is expected to have two keys: `operation_id` and `variables`. The `operation_id`
        is the ID of the operation to be performed, while the `variables` key contains the variables
        :type body: json
        :return: a JSON response with a developer message and data containing the result of the
        operation.
        """
        operation_id = body['operation_id']
        variables = self.get_variables(body['variables'])
        try:
            operation = Operation.objects.get(id=operation_id)
            user_balance, new_user_balance = self.check_balance(request.user, operation)
            if new_user_balance >= 0:
                self.check_variable_payload(variables, operation)
                # Perform the operation using the corresponding function
                operation_function = operation_functions[operation.type]
                result = operation_function(**variables)
                
                record_payload = {
                    "operation": operation,
                    "user": request.user,
                    "amount": operation.cost,
                    "operation_response": str(result)
                }
                record = Record(**record_payload)
                record.user_balance = new_user_balance
                request.user.balance = new_user_balance
                record.save()
                request.user.save()
                
                return JsonResponse({'developer_message': f'The process {operation.type} was successful',
                                        'data': {'result': result, 'variables': variables}})
            else:
                raise OutOfMoney(f"User balance({user_balance}) is not enough to perform an operation({operation.type}) of {operation.cost}")
        except ObjectDoesNotExist:
            raise NotFound

# This is a paginated view class for the Operation model with allowed filters for type and cost range.
class GetOperations(PaginatedView):
    allowed_order_filters = ['type', 'cost__gt', 'cost__lt']
    model = Operation

# This is a paginated view class for retrieving user records with allowed filters and search fields.
class GetUserRecords(PaginatedView):
    allowed_order_filters = ['id', 'user_id', 'amount', 'amount__lt', 'amount__gt', 'operation__type', 'operation__cost', 'operation__cost__lt', 'operation__cost__gt', 'user__username', 'user_balance', 'user_balance__lt', 'user_balance__gt', 'operation_response', 'created_at']
    search_fields = ['operation__type', 'user__username', 'operation__cost', 'user_balance', 'operation_response']
    model = Record

    def process_request(self, request, body, *args, **kwargs):
        response = super().process_request(request, body, *args, **kwargs)
        return add_success_response(response, 'user_balance', round(request.user.balance,2))
        

class DeleteRecord(BaseAuthView):
    model = Record
    required_fields = ['id']
