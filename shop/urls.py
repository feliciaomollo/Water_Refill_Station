from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_base, name='test_base'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/edit/', views.customer_update, name='customer_update'), #What <int:pk> means: this is a URL parameter — it captures whatever number appears in that position in the URL (e.g. /customers/3/edit/ captures 3)
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/add/', views.sale_create, name='sale_create'),
    path('sales/<int:pk>/edit/', views.sale_update, name='sale_update'),
    path('sales/<int:pk>/delete/', views.sale_delete, name='sale_delete'),
    path('', views.dashboard, name='dashboard'),
]
