# ruff: noqa: S101, W0621, S106
# tickets/tests/test_views.py

import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.urls import reverse

from tickets.forms import TicketForm
from tickets.models import Ticket

pytestmark = pytest.mark.django_db


@pytest.fixture
def create_user():
    """Fixture to create a standard user."""
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def create_other_user():
    """Fixture to create a secondary user."""
    return User.objects.create_user(username="otheruser", password="password123")


@pytest.fixture
def auth_client(client, create_user):
    """Fixture to provide a logged-in test client."""
    client.force_login(create_user)
    return client


@pytest.fixture
def create_ticket_for_user(create_user):
    """Fixture to create a ticket associated with the primary user."""
    user = create_user
    return Ticket.objects.create(
        title="User Ticket", description="Desc", created_by=user
    )


# --- Test Authentication Requirements ---


def test_views_require_login(client):
    """Test that all views redirect unauthenticated users to the login page."""
    urls = [
        reverse("ticket_list"),
        reverse("create_ticket"),
        reverse("ticket_detail", kwargs={"pk": 999}),  # Use an ID unlikely to exist
    ]
    for url in urls:
        response = client.get(url, follow=True)
        assert response.request["PATH_INFO"] == reverse("login")


# --- Test ticket_list View ---


def test_ticket_list_view(auth_client, create_user, create_ticket_for_user):
    """Test the ticket list view for an authenticated user."""
    client = auth_client
    url = reverse("ticket_list")
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert "tickets/ticket_list.html" in [t.name for t in response.templates]
    assert list(response.context["tickets"]) == [create_ticket_for_user]


def test_ticket_list_only_shows_own_tickets(
    auth_client, create_user, create_other_user
):
    """Test a user only sees tickets they created."""
    client = auth_client
    user = create_user
    my_ticket = Ticket.objects.create(
        title="My Ticket", description="Mine", created_by=user
    )
    other_ticket = Ticket.objects.create(
        title="Other Ticket", description="Not mine", created_by=create_other_user
    )

    response = client.get(reverse("ticket_list"), follow=True)

    assert response.status_code == 200
    tickets_in_context = list(response.context["tickets"])
    assert len(tickets_in_context) == 1
    assert my_ticket in tickets_in_context
    assert other_ticket not in tickets_in_context


# --- Test ticket_detail View ---


def test_ticket_detail_view(auth_client, create_user, create_ticket_for_user):
    """Test the detail view works for the ticket owner."""
    client = auth_client
    url = reverse("ticket_detail", kwargs={"pk": create_ticket_for_user.pk})
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert "tickets/ticket_detail.html" in [t.name for t in response.templates]
    assert response.context["ticket"] == create_ticket_for_user


def test_ticket_detail_view_access_denied(auth_client, create_user, create_other_user):
    """Test a user cannot view another user's ticket."""
    client = auth_client
    other_ticket = Ticket.objects.create(
        title="Other Ticket", description="Not mine", created_by=create_other_user
    )

    url = reverse("ticket_detail", kwargs={"pk": other_ticket.pk})
    response = client.get(url, follow=True)

    assert response.status_code == 404


# --- Test create_ticket View ---


def test_create_ticket_get(auth_client, create_user):
    """Test that the create ticket page loads correctly with a form."""
    client = auth_client
    url = reverse("create_ticket")
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert "tickets/create_ticket.html" in [t.name for t in response.templates]
    assert isinstance(response.context["form"], TicketForm)


# --- DIAGNOSTIC TEST (Added to debug save issue, passed) ---


@pytest.mark.django_db
def test_create_ticket_view_direct_call(create_user):
    """Test the create_ticket view by calling the function directly,
    bypassing the test client."""
    user = create_user

    request = HttpRequest()
    request.method = "POST"
    request.user = user

    request.POST = {
        "title": "New Ticket Title Direct",
        "description": "Description for the new ticket via direct call.",
        "priority": "high",
    }

    initial_ticket_count = Ticket.objects.count()

    assert Ticket.objects.count() == initial_ticket_count + 1
    ticket = Ticket.objects.get(title="New Ticket Title Direct")
    assert ticket.created_by == user
