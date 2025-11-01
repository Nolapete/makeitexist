# tickets/forms.py

from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "priority"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                "placeholder": "Enter ticket title"
            }),
            "description": forms.Textarea(attrs={
                "class": "block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                "rows": 4,
                "placeholder": "Describe the issue or request in detail"
            }),
            "priority": forms.Select(attrs={
                "class": "block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            }),
        }


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "priority", "status"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                "placeholder": "Enter ticket title"
            }),
            "description": forms.Textarea(attrs={
                "class": "block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                "rows": 4,
                "placeholder": "Describe the issue or request in detail"
            }),
            "priority": forms.Select(attrs={
                "class": "block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            }),
            "status": forms.Select(attrs={
                "class": "block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            }),
        }
