# ruff: noqa: S101, W0621, S106
import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse

from tickets.models import Ticket

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_user():
    """Fixture to create a superuser for admin access."""
    return User.objects.create_superuser(
        username="admin", email="admin@example.com", password="password"
    )


def test_ticket_model_registered_in_admin():
    """Verify that the Ticket model is correctly registered with the admin site."""
    assert admin.site.is_registered(Ticket) is True


def test_admin_changelist_view(admin_client, admin_user):
    """Test that the main change list view for Tickets loads successfully."""
    url = reverse("admin:tickets_ticket_changelist")
    # Follow redirects caused by SECURE_SSL_REDIRECT
    response = admin_client.get(url, follow=True)
    assert response.status_code == 200


def test_admin_add_view(admin_client):
    """Test that the 'add ticket' view loads successfully."""
    url = reverse("admin:tickets_ticket_add")
    response = admin_client.get(url, follow=True)
    assert response.status_code == 200


def test_admin_change_view(admin_client, admin_user):
    """Test that the 'change ticket' view loads successfully for an existing ticket."""
    ticket = Ticket.objects.create(
        title="Test Ticket", description="Desc", created_by=admin_user
    )
    url = reverse("admin:tickets_ticket_change", args=[ticket.pk])
    response = admin_client.get(url, follow=True)
    assert response.status_code == 200


def test_admin_delete_view(admin_client, admin_user):
    """Test that the 'delete ticket' view loads successfully."""
    ticket = Ticket.objects.create(
        title="Test Ticket", description="Desc", created_by=admin_user
    )
    url = reverse("admin:tickets_ticket_delete", args=[ticket.pk])
    response = admin_client.get(url, follow=True)
    assert response.status_code == 200
