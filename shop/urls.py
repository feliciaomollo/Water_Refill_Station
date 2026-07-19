from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import TankLevelAPIView


urlpatterns = [
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
    path('debts/', views.debt_list, name='debt_list'),
    path('debts/<int:pk>/mark-paid/', views.mark_paid, name='mark_paid'),
    path('debts/<int:pk>/send-sms/', views.send_sms_view, name='send_sms'),
    path('tank-level/entry/', views.tank_level_entry, name='tank_level_entry'),
    path('api/tank-level/', TankLevelAPIView.as_view(), name='tank_level_api'), # TankLevelAPIView is a class-based view, not a function-based view, so it can't be referenced as views.TankLevelAPIView the same way your other views are — you need to import it explicitly by name.
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sales/<int:pk>/cancel/', views.sale_cancel, name='sale_cancel'),
    path('sales/<int:pk>/restore/', views.sale_restore, name='sale_restore'),
    path('password-reset/', 
    auth_views.PasswordResetView.as_view(
        template_name='shop/password_reset.html'
    ), 
    name='password_reset'),

    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='shop/password_reset_done.html'
        ), 
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='shop/password_reset_confirm.html'
        ), 
        name='password_reset_confirm'),

    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='shop/password_reset_complete.html'
        ), 
        name='password_reset_complete'),
]


