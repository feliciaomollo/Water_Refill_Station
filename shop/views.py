from datetime import date
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Product, Sale
from .forms import CustomerForm, ProductForm, SaleForm

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

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'shop/customer_form.html', {'form': form})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'shop/customer_confirm_delete.html', {'customer': customer})

def product_list(request):
    products = Product.objects.all()     
    return render(request, 'shop/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})

def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)  
            sale.total_amount = sale.quantity * sale.product.price
            sale.save()
            return redirect('sale_list')
    else:
        form = SaleForm()
    return render(request, 'shop/sale_form.html', {'form': form})

def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'shop/sale_list.html', {'sales': sales})

def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            sale = form.save(commit=False)  
            sale.total_amount = sale.quantity * sale.product.price
            sale.save()
            return redirect('sale_list')
    else:
        form = SaleForm(instance=sale)
    return render(request, 'shop/sale_form.html', {'form': form})

def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('sale_list')
    return render(request, 'shop/sale_confirm_delete.html', {'sale': sale})

def dashboard(request):
    today = date.today()

    # 1. Today's sales count
    today_sales_count = Sale.objects.filter(date__date=today).count()

    # 2. Today's total revenue
    today_revenue = Sale.objects.filter(
        date__date=today
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # 3. Unpaid sales count
    unpaid_count = Sale.objects.filter(is_paid=False).count()

    # 4. Total outstanding amount
    outstanding_amount = Sale.objects.filter(
        is_paid=False
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # 5. All products for stock summary
    products = Product.objects.all()

    context = {
        'today_sales_count': today_sales_count,
        'today_revenue': today_revenue,
        'unpaid_count': unpaid_count,
        'outstanding_amount': outstanding_amount,
        'products': products,
    }
    return render(request, 'shop/dashboard.html', context)