from django import forms

from .models import Location, PantryItem, StorageUnit


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name", "address"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., Home, Office"}
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Optional address",
                }
            ),
        }


class StorageUnitForm(forms.ModelForm):
    class Meta:
        model = StorageUnit
        fields = ["name", "unit_type", "temperature", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "unit_type": forms.Select(attrs={"class": "form-control"}),
            "temperature": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1"}
            ),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        help_texts = {
            "temperature": "Temperature in Celsius.",
        }


class PantryItemForm(forms.ModelForm):
    class Meta:
        model = PantryItem
        fields = ["name", "category", "barcode", "default_storage", "min_stock_level"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "barcode": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., 123456789012"}
            ),
            "default_storage": forms.Select(attrs={"class": "form-control"}),
            "min_stock_level": forms.NumberInput(
                attrs={"class": "form-control", "min": "1"}
            ),
        }
