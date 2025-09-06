from django.contrib import admin
from .models import Customer, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "company", "created_at")
    search_fields = ("name", "email", "phone", "company")
    list_filter = ("created_at",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "service_type", "status", "created_at")
    list_filter = ("status", "service_type", "created_at")
    search_fields = ("customer__name", "description")
    autocomplete_fields = ("customer",)

# Register your models here.
