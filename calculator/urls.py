from django.urls import path
from .views.user_views import LoginView, LogoutView
from .views.record_views import NewOperationView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('newoperation', NewOperationView.as_view(), name='new_operation'),
]
