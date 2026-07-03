from django import forms
from .models import Customer, Product

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer      
        fields = ['name', 'location', 'phone_number', 'is_credit_customer']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product      
        fields = ['size', 'prize', 'stock_quantity']