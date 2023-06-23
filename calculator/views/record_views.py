from wsgiref.simple_server import WSGIRequestHandler
from django.http import JsonResponse
import json
from django.core.exceptions import ObjectDoesNotExist
from calculator import BASE_USER_BALANCE
from calculator.exceptions import NotFound
from calculator.models import Operation, Record, User
from calculator.views import BaseAuthView

class NewOperationView(BaseAuthView):
    required_fields = ['operation_id', 'amount']

    @staticmethod
    def get_amount(amount):
        try:
            amount = amount if amount else "{}"
            amount = json.loads(amount)
        except:
            amount = {}
        if not amount:
            amount = {}
        return amount
    
    @staticmethod
    def check_balance(record: Record, user: User, operation: Operation):
        last_record = Record.objects.filter(user=user).order_by("-created_at").first()
        record.user_balance = (last_record.user_balance if last_record else BASE_USER_BALANCE) - operation.cost

    def process_request(self, request: WSGIRequestHandler, body: json):
        operation_id = body['operation_id']
        amount = self.get_amount(body['amount'])
        try:
            operation = Operation.objects.get(id=operation_id)
            if operation.type == 'addition':
                # Perform addition operation
                result = float(amount['A']) + float(amount['B'])
                record_payload = {
                    "operation": operation,
                    "user": request.user,
                    "amount": amount,
                    "operation_response": str(result)
                }
                record = Record(**record_payload)
            self.check_balance(record, request.user, operation)
            record.save()
            return JsonResponse({'developer_message': f'The proccess {operation.type} done successfully', 'data': {'result': result}})
        except ObjectDoesNotExist:
            raise NotFound
        except Exception as e:
            breakpoint()
            raise JsonResponse({'developer_message': str(e)}, status=500)

