from django.urls import path

from calculator.views import ApiStatusView
from .views.user_views import LoginView, LogoutView, UserView
from .views.operation_views import (
    NewOperationView,
    GetOperations,
    GetUserRecords,
    DeleteRecord,
)

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("record", NewOperationView.as_view(), name="new_operation_record"),
    path("operations", GetOperations.as_view(), name="get_operations"),
    path("records", GetUserRecords.as_view(), name="get_records"),
    path("record/delete", DeleteRecord.as_view(), name="delete_record"),
    path("user", UserView.as_view(), name="get_user_info"),
    path("status/", ApiStatusView.as_view(), name="get_api_status"),
]
