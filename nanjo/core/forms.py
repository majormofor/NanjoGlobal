from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import ContactMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Send Message", css_class="btn btn-primary"))


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(label="Full name", max_length=255)
    phone = forms.CharField(max_length=50, required=False)
    company = forms.CharField(max_length=255, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "full_name", "phone", "company", "address", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Create Account"))

