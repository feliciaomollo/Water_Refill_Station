from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_base, name='test_base'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
]