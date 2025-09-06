from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Customer, Order


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone", "company", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "service_type", "description", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))

