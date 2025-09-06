from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from .models import Customer, Order
from .forms import CustomerForm, OrderForm


def staff_required(view_func):
    return login_required(user_passes_test(lambda u: u.is_staff, login_url='login')(view_func))


@staff_required
def dashboard(request):
    total_customers = Customer.objects.count()
    active_orders = Order.objects.exclude(status=Order.Status.COMPLETED).count()
    status_counts = Order.objects.values('status').annotate(total=Count('status'))
    recent_orders = Order.objects.select_related('customer').order_by('-created_at')[:10]
    context = {
        'total_customers': total_customers,
        'active_orders': active_orders,
        'status_counts': status_counts,
        'recent_orders': recent_orders,
    }
    return render(request, 'crm/dashboard.html', context)


@staff_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-created_at')
    return render(request, 'crm/customer_list.html', {'customers': customers})


@staff_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created')
            return redirect('crm:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'crm/customer_form.html', {'form': form})


@staff_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated')
            return redirect('crm:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'crm/customer_form.html', {'form': form})


@staff_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted')
        return redirect('crm:customer_list')
    return render(request, 'crm/customer_confirm_delete.html', {'customer': customer})


@staff_required
def order_list(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = customer.orders.all().order_by('-created_at')
    return render(request, 'crm/order_list.html', {'customer': customer, 'orders': orders})


@staff_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            messages.success(request, 'Order created')
            return redirect('crm:customer_list')
    else:
        form = OrderForm()
    return render(request, 'crm/order_form.html', {'form': form})


@staff_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated')
            return redirect('crm:customer_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'crm/order_form.html', {'form': form})


@staff_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted')
        return redirect('crm:customer_list')
    return render(request, 'crm/order_confirm_delete.html', {'order': order})

# Create your views here.
