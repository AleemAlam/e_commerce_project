from django.urls import path, include
from . import views
urlpatterns = [
    path('transaction/', views.Transaction.as_view()),
    path('check_transaction/', views.TransactionStatus.as_view()),
]