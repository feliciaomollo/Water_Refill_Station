from django.shortcuts import render
from .models import Customer

def test_base(request):
    return render(request, 'shop/base.html')

def customer_list(request):
    customers = Customer.objects.all()     
    return render(request, 'shop/customer_list.html', {'customers': customers})