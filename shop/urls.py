from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_base, name='test_base'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/edit/', views.customer_update, name='customer_update'), #What <int:pk> means: this is a URL parameter — it captures whatever number appears in that position in the URL (e.g. /customers/3/edit/ captures 3)
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
]