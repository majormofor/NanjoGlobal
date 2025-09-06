from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login
from .models import ContactMessage
from .forms import ContactForm, SignupForm
from crm.models import Customer
from django.conf import settings  # <-- Add this



def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/about.html')


def services(request):
    return render(request, 'core/services.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message_obj = form.save()
            # Ensure customer and order are created for contact
            from crm.models import Customer, Order
            customer, _ = Customer.objects.get_or_create(
                email=message_obj.email,
                defaults={
                    'name': message_obj.name,
                    'phone': message_obj.phone,
                    'address': '',
                },
            )
            Order.objects.create(
                customer=customer,
                service_type='customs_documentation',
                description=f"Contact form message: {message_obj.message}",
                status=Order.Status.PENDING,
            )

            # Email notification
            try:
                send_mail(
                    subject='New Contact Message - Nanjo Global Logistics',
                    message=(
                        f"Name: {message_obj.name}\n"
                        f"Email: {message_obj.email}\n"
                        f"Phone: {message_obj.phone}\n\n"
                        f"Message:\n{message_obj.message}\n"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['moformajor@gmail.com'],
                    fail_silently=False,  # set to True in production
                )
            except Exception as e:
                messages.error(request, f"Error sending email: {e}")

            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a matching Customer profile record
            Customer.objects.create(
                name=form.cleaned_data.get('full_name') or user.get_username(),
                email=form.cleaned_data.get('email'),
                phone=form.cleaned_data.get('phone'),
                company=form.cleaned_data.get('company'),
                address=form.cleaned_data.get('address'),
            )
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('core:home')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

# Create your views here.
