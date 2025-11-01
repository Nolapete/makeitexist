# tickets/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.ticket_list, name="ticket_list"),
    path("ticket/new/", views.create_ticket, name="create_ticket"),
    path("ticket/<int:pk>/", views.ticket_detail, name="ticket_detail"),
]
