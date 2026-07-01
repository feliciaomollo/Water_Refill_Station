from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer      
        fields = ['name', 'location', 'phone_number', 'is_credit_customer']