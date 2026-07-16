from datetime import date
from decouple import config
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from .models import Customer, Product, Sale, TankLevel
from .forms import CustomerForm, ProductForm, SaleForm, TankLevelForm
from .sms import send_sms
from .serializers import TankLevelSerializer

def test_base(request):
    return render(request, 'shop/base.html')

@login_required #if the user isn't logged in, Django automatically redirects them to the login page. If they are logged in, the view runs normally.
def customer_list(request):
    customers = Customer.objects.all()   
    return render(request, 'shop/customer_list.html', {'customers': customers})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer {form.instance.name} added successfully.")
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'shop/customer_form.html', {'form': form})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer {customer.name} updated successfully.")
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'shop/customer_form.html', {'form': form})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        try:
            customer.delete()
            messages.success(request, f"{customer.name} deleted successfully.")
        except ProtectedError:
            messages.error(request, f"Cannot delete {customer.name} — they have existing sales records. Delete their sales first.")
        return redirect('customer_list')
    return render(request, 'shop/customer_confirm_delete.html', {'customer': customer})

@login_required
def product_list(request):
    products = Product.objects.all()     
    return render(request, 'shop/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('product_list')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})

@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)  
            sale.total_amount = sale.quantity * sale.product.price
            sale.save()
            messages.success(request, f"Sale recorded — KES {sale.total_amount} total.")
            return redirect('sale_list')
    else:
        form = SaleForm()
    return render(request, 'shop/sale_form.html', {'form': form})

@login_required
def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'shop/sale_list.html', {'sales': sales})

@login_required
def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            sale = form.save(commit=False)  
            sale.total_amount = sale.quantity * sale.product.price
            sale.save()
            messages.success(request, "Sale updated successfully.")
            return redirect('sale_list')
    else:
        form = SaleForm(instance=sale)
    return render(request, 'shop/sale_form.html', {'form': form})

@login_required
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        messages.success(request, "Sale deleted successfully.")
        return redirect('sale_list')
    return render(request, 'shop/sale_confirm_delete.html', {'sale': sale})

@login_required
def sale_cancel(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.is_cancelled = True
        sale.save()
        messages.success(request, f"Sale for {sale.customer.name} has been cancelled.")
        return redirect('sale_list')
    return render(request, 'shop/sale_cancel_confirm.html', {'sale': sale})

@login_required
def sale_restore(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.is_cancelled = False
        sale.save()
        messages.success(request, f"Sale for {sale.customer.name} has been restored.")
        return redirect('sale_list')
    return redirect('sale_list')

@login_required
def dashboard(request):
    today = date.today()
    today_sales_count = Sale.objects.filter(
        date__date=today, is_cancelled=False
    ).count()

    today_revenue = Sale.objects.filter(
        date__date=today, is_cancelled=False
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    unpaid_count = Sale.objects.filter(
        is_paid=False, is_cancelled=False
    ).count()

    outstanding_amount = Sale.objects.filter(
        is_paid=False, is_cancelled=False
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Latest tank level
    latest_tank = TankLevel.objects.order_by('-recorded_at').first()

    products = Product.objects.all()

    context = {
        'today_sales_count': today_sales_count,
        'today_revenue': today_revenue,
        'unpaid_count': unpaid_count,
        'outstanding_amount': outstanding_amount,
        'products': products,
        'latest_tank': latest_tank,
    }
    return render(request, 'shop/dashboard.html', context)

@login_required
def debt_list(request):
    customers_in_debt = Customer.objects.filter(
    sale__is_paid=False,
    sale__is_cancelled=False
    ).annotate(
        total_owed=Sum('sale__total_amount',
        filter=Q(sale__is_paid=False, sale__is_cancelled=False))
    ).distinct()

    context = {'customers_in_debt': customers_in_debt}
    return render(request, 'shop/debt_list.html', context)

@login_required
def mark_paid(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        Sale.objects.filter(
            customer=customer,
            is_paid=False
        ).update(is_paid=True)
        messages.success(request, f"All sales for {customer.name} marked as paid.")
        return redirect('debt_list')
    return render(request, 'shop/mark_paid_confirm.html', {'customer': customer})

@login_required
def send_sms_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        message = request.POST.get('message')
        phone = customer.phone_number
        result = send_sms(phone, message)
        if result['success']:
            messages.success(request, f"SMS sent successfully to {customer.phone_number}.")
            return redirect('debt_list')
        else:
            messages.error(request, f"Failed to send SMS: {result['error']}")
            return render(request, 'shop/send_sms.html', {'customer': customer})
    return render(request, 'shop/send_sms.html', {'customer': customer})

#only works on function-based views 
class TankLevelAPIView(APIView):
    def post(self, request):
        serializer = TankLevelSerializer(data=request.data)
        if serializer.is_valid():
            tank_level = serializer.save(source='api')
            
            # Send SMS alert if level is below 20%
            if tank_level.level_percentage < 20:
                owner_phone = config('OWNER_PHONE')
                send_sms(
                    owner_phone,
                    f"WARNING: Water tank level is critically low at {tank_level.level_percentage}%. Please arrange a refill immediately."
                )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required    
def tank_level_entry(request):
    if request.method == 'POST':
        form = TankLevelForm(request.POST)
        if form.is_valid():
            tank = form.save(commit=False)
            tank.source = 'manual'
            tank.save()

            # Send SMS alert if level is below 20%
            if tank.level_percentage < 20:
                owner_phone = config('OWNER_PHONE')
                send_sms(
                    owner_phone,
                    f"WARNING: Water tank level is low at {tank.level_percentage}%. Please arrange a refill."
                )
            return redirect('dashboard')
    else:
        form = TankLevelForm()
    return render(request, 'shop/tank_level_form.html', {'form': form})