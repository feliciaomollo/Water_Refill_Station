from django import forms
from .models import Customer, Product, Sale, TankLevel

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer      
        fields = ['name', 'location', 'phone_number', 'is_credit_customer']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product      
        fields = ['size', 'price', 'stock_quantity']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale      
        fields = ['customer', 'product', 'quantity']

class TankLevelForm(forms.ModelForm):
    class Meta:
        model = TankLevel
        fields = ['level_percentage']