from django.urls import path
from .views.user_views import LoginView, LogoutView
from .views.operation_views import NewOperationView, GetOperations, GetUserRecords, DeleteRecord

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('record', NewOperationView.as_view(), name='new_operation_record'),
    path('operations', GetOperations.as_view(), name='get_operations'),
    path('records', GetUserRecords.as_view(), name='get_records'),
    path('record/delete', DeleteRecord.as_view(), name='delete_record'),
]
