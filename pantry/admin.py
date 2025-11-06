# pantry/admin.py

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import ItemCategory, Location, PantryItem, Stock, StorageUnit

# =============================================================================
# 1. Utility Functions (DRY)
# =============================================================================


def fahrenheit_to_celsius(f):
    """Convert °F to °C"""
    return round((f - 32) * 5.0 / 9.0, 1) if f is not None else None


def celsius_to_fahrenheit(c):
    """Convert °C to °F"""
    return round((c * 9.0 / 5.0) + 32, 1) if c is not None else None


# =============================================================================
# 2. Custom Admin Form: StorageUnit with Dual Temp Input
# =============================================================================


class StorageUnitAdminForm(forms.ModelForm):
    temperature_celsius = forms.DecimalField(
        max_digits=6,
        decimal_places=1,
        required=False,
        label="Temperature (°C)",
        help_text="Enter in Celsius. Automatically saved to database.",
    )
    temperature_fahrenheit = forms.DecimalField(
        max_digits=6,
        decimal_places=1,
        required=False,
        label="Temperature (°F)",
        help_text="Enter in Fahrenheit. Will be converted to Celsius.",
    )

    class Meta:
        model = StorageUnit
        fields = ["name", "unit_type", "location", "notes"]  # Handled by clean()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        celsius = self.instance.temperature
        self.fields["temperature_celsius"].initial = celsius
        self.fields["temperature_fahrenheit"].initial = (
            celsius_to_fahrenheit(celsius) if celsius else None
        )

    def clean(self):
        cleaned_data = super().clean()
        celsius = cleaned_data.get("temperature_celsius")
        fahrenheit = cleaned_data.get("temperature_fahrenheit")

        # Prefer Celsius; fallback to Fahrenheit
        if celsius is not None:
            cleaned_data["temperature"] = celsius
        elif fahrenheit is not None:
            cleaned_data["temperature"] = fahrenheit_to_celsius(fahrenheit)
        else:
            cleaned_data["temperature"] = None

        return cleaned_data


# =============================================================================
# 3. Inlines
# =============================================================================


class StockInline(admin.TabularInline):
    """Inline for stock items inside StorageUnit"""

    model = Stock
    extra = 1
    fields = ("item", "quantity", "expiry_date", "status")
    readonly_fields = ("status",)
    show_change_link = True
    classes = ["collapse"]

    def status(self, obj):
        if obj.is_expired():
            return format_html('<span style="color: red;">❌ Expired</span>')
        days = obj.days_until_expiry()
        if days is not None and days <= 7:
            return format_html('<span style="color: orange;">⚠️ {} days</span>', days)
        return format_html('<span style="color: green;">✅ OK</span>')

    status.short_description = "Status"


class StorageUnitInline(admin.StackedInline):
    """Inline for storage units inside Location"""

    model = StorageUnit
    form = StorageUnitAdminForm
    extra = 1
    fields = (
        ("name", "unit_type"),
        ("temperature_celsius", "temperature_fahrenheit"),
        "notes",
    )
    classes = ["collapse"]
    verbose_name = "Storage Unit"
    verbose_name_plural = "Storage Units"


# =============================================================================
# 4. Admin Classes
# =============================================================================


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "unit_count", "created_by", "created_at")
    list_filter = ("created_at", "created_by")
    search_fields = ("name", "address")
    readonly_fields = ("created_at",)
    inlines = [StorageUnitInline]
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def unit_count(self, obj):
        return obj.storage_units.count()

    unit_count.short_description = "Units"


@admin.register(StorageUnit)
class StorageUnitAdmin(admin.ModelAdmin):
    form = StorageUnitAdminForm
    inlines = [StockInline]
    list_display = (
        "name",
        "unit_type",
        "location",
        "temperature_display",
        "item_count",
        "notes_preview",
    )
    list_filter = ("unit_type", "location")
    search_fields = ("name", "location__name", "notes")

    fieldsets = (
        (None, {"fields": ("name", "unit_type", "location")}),
        (
            "Temperature Settings",
            {
                "fields": ("temperature_celsius", "temperature_fahrenheit"),
                "description": "Enter temperature in Celsius or Fahrenheit. "
                "Automatically converted and stored in Celsius.",
            },
        ),
        ("Additional Info", {"fields": ("notes",), "classes": ("collapse",)}),
    )

    def temperature_display(self, obj):
        """Show temperature in both °C and °F"""
        if obj.temperature is not None:
            c = obj.temperature
            f = celsius_to_fahrenheit(c)
            return format_html("{} °C / {} °F", c, f)
        return format_html('<span style="color: gray;">Not set</span>')

    temperature_display.short_description = "Temperature"

    def item_count(self, obj):
        """Number of stock items in this unit"""
        return obj.stocks.count()

    item_count.short_description = "Items"

    def notes_preview(self, obj):
        """Short preview of notes for list view"""
        if obj.notes:
            return obj.notes if len(obj.notes) < 50 else obj.notes[:47] + "..."
        return format_html('<span style="color: gray;">—</span>')

    notes_preview.short_description = "Notes"


@admin.register(PantryItem)
class PantryItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "min_stock_level",
        "stock_status",
        "item_count",
        "created_by",
    )
    list_filter = ("category", "created_by", "min_stock_level")
    search_fields = ("name", "barcode", "category__name")
    readonly_fields = ("created_by",)
    autocomplete_fields = ("category", "default_storage")

    fieldsets = (
        (None, {"fields": ("name", "category", "barcode")}),
        (
            "Storage & Stocking",
            {
                "fields": ("default_storage", "min_stock_level"),
                "description": "Set default storage unit and desired stock level.",
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """Automatically set created_by on save"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def stock_status(self, obj):
        """Overall stock status: OK, Low, or Out"""
        total = sum(stock.quantity for stock in obj.stocks.all())
        if total == 0:
            return format_html('<span style="color: red;">🔴 Out</span>')
        if total < obj.min_stock_level:
            return format_html('<span style="color: orange;">🟡 Low</span>')
        return format_html('<span style="color: green;">🟢 OK</span>')

    stock_status.short_description = "Status"

    def item_count(self, obj):
        """Total quantity across all storage units"""
        return sum(stock.quantity for stock in obj.stocks.all())

    item_count.short_description = "Total Qty"


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "storage_unit",
        "quantity",
        "purchase_date",
        "expiry_date",
        "days_until_expiry",
        "status",
    )
    list_filter = (
        "storage_unit__location",
        "storage_unit__unit_type",
        "purchase_date",
        "expiry_date",
    )
    search_fields = ("item__name", "storage_unit__name", "batch_number")
    date_hierarchy = "purchase_date"
    raw_id_fields = ("item", "storage_unit")

    def days_until_expiry(self, obj):
        days = obj.days_until_expiry()
        if days is None:
            return "No expiry"
        return f"{days} days" if days > 0 else "Expired"

    days_until_expiry.short_description = "Days to Expiry"

    def status(self, obj):
        if obj.is_expired():
            return format_html('<span style="color: red;">❌ Expired</span>')
        days = obj.days_until_expiry()
        if days is not None and days <= 7:
            return format_html('<span style="color: orange;">⚠️ Expires Soon</span>')
        return format_html('<span style="color: green;">✅ OK</span>')

    status.short_description = "Status"

    # Improve form layout
    fieldsets = (
        (None, {"fields": ("item", "storage_unit")}),
        ("Stock Details", {"fields": ("quantity", "purchase_date", "batch_number")}),
        ("Expiry (Optional)", {"fields": ("expiry_date",), "classes": ("collapse",)}),
    )

    # Set default ordering
    ordering = ("expiry_date",)

    # Improve display in admin
    readonly_fields = ("purchase_date",)  # if you want to auto-set this


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "item_count")
    search_fields = ("name",)

    def item_count(self, obj):
        return obj.pantryitem_set.count()

    item_count.short_description = "Items"


# Customize Django Admin Title
admin.site.site_header = "Pantry Management Admin"
admin.site.site_title = "Pantry Admin"
admin.site.index_title = "Welcome to the Pantry Admin Portal"
