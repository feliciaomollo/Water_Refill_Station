from django.shortcuts import render, redirect
from .models import Customer
from .forms import CustomerForm

def test_base(request):
    return render(request, 'shop/base.html')

def customer_list(request):
    customers = Customer.objects.all()     
    return render(request, 'shop/customer_list.html', {'customers': customers})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'shop/customer_form.html', {'form': form})