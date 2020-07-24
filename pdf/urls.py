from django.urls import path, include
from . import views
urlpatterns = [
    path('convert_to_pdf/', views.CreateInvoiceToPDF.as_view()),
]