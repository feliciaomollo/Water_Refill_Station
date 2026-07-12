from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, Row, Column, Field
from .models import Customer, Product, Sale, TankLevel

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'location', 'phone_number', 'is_credit_customer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('phone_number', css_class='col-md-6'),
            ),
            Field('location'),
            Field('is_credit_customer'),
            Submit('submit', 'Save', css_class='btn btn-primary mt-2'),
        )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['size', 'price', 'stock_quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('size'),
            Row(
                Column('price', css_class='col-md-6'),
                Column('stock_quantity', css_class='col-md-6'),
            ),
            Submit('submit', 'Save', css_class='btn btn-primary mt-2'),
        )

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('customer'),
            Field('product'),
            Field('quantity'),
            Submit('submit', 'Save', css_class='btn btn-primary mt-2'),
        )

class TankLevelForm(forms.ModelForm):
    class Meta:
        model = TankLevel
        fields = ['level_percentage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('level_percentage'),
            Submit('submit', 'Save Reading', css_class='btn btn-primary mt-2'),
        )