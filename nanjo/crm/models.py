from django.db import models
from django.contrib.auth import get_user_model


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    SERVICE_TYPES = [
        ("import_export", "Import & Export Clearing"),
        ("freight_forwarding", "Freight Forwarding"),
        ("customs_documentation", "Customs Documentation"),
        ("warehousing_distribution", "Warehousing & Distribution"),
        ("delivery_solutions", "Delivery Solutions"),
    ]

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='orders')
    service_type = models.CharField(max_length=64, choices=SERVICE_TYPES)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.get_service_type_display()} - {self.customer.name}"

# Create your models here.
