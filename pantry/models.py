from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import date, timedelta


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StorageUnit(models.Model):
    UNIT_TYPES = [
        ("freezer", "Freezer"),
        ("refrigerator", "Refrigerator"),
        ("closet", "Closet"),
        ("cabinet", "Cabinet"),
        ("pantry", "Pantry"),
    ]

    name = models.CharField(max_length=100)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="storage_units"
    )
    temperature = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_unit_type_display()} - {self.name} ({self.location})"


class ItemCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "ItemCategories"

    def __str__(self):
        return self.name


class PantryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        ItemCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)
    default_storage = models.ForeignKey(
        StorageUnit, on_delete=models.SET_NULL, null=True, blank=True
    )
    min_stock_level = models.PositiveIntegerField(
        default=1, help_text="Minimum quantity to keep in stock"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    min_stock_alert = models.BooleanField(
        default=True, help_text="Enabled out-of-stock alerts"
    )
    expiry_alert_days = models.PositiveIntegerField(
        default=7, help_text="Number of days before expiry to send alert"
    )

    def __str__(self):
        return self.name


class Stock(models.Model):
    item = models.ForeignKey(
        PantryItem, on_delete=models.CASCADE, related_name="stocks"
    )
    storage_unit = models.ForeignKey(
        StorageUnit, on_delete=models.CASCADE, related_name="stocks"
    )  # ✅ Add this
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField(blank=True, null=True)
    purchase_date = models.DateField(default=date.today)
    batch_number = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Stock"

    def is_expired(self):
        return self.expiry_date and self.expiry_date < date.today()

    def days_until_expiry(self):
        if not self.expiry_date:
            return None
        return (self.expiry_date - date.today()).days

    def __str__(self):
        return f"{self.item.name} - {self.quantity} in {self.storage_unit}"
