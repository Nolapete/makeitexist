# tickets/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.ticket_list, name="ticket_list"),
    path("ticket/new/", views.create_ticket, name="create_ticket"),
    path("ticket/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("ticket/<int:pk>/update/", views.update_ticket, name="update_ticket"),
    path("ticket/<int:pk>/resolve/", views.resolve_ticket, name="resolve_ticket"),
    path("ticket/<int:pk>/close/", views.close_ticket, name="close_ticket"),
]
