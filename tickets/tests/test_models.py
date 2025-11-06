# ruff: noqa: S101, W0621, S106

import pytest
from django.contrib.auth.models import User

from tickets.models import PRIORITY_CHOICES, STATUS_CHOICES, Ticket

pytestmark = pytest.mark.django_db


@pytest.fixture
def create_user():
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def create_assigned_user():
    return User.objects.create_user(username="assigneduser", password="password123")


def test_ticket_creation(create_user):
    user = create_user
    ticket = Ticket.objects.create(
        title="My first ticket",
        description="This is a test description.",
        created_by=user,
    )

    assert ticket.id is not None
    assert ticket.title == "My first ticket"
    assert ticket.description == "This is a test description."
    assert ticket.status == "open"
    assert ticket.priority == "medium"
    assert ticket.created_by == user
    assert ticket.assigned_to is None
    assert ticket.__str__() == "My first ticket"


def test_ticket_with_assignment(create_user, create_assigned_user):
    creator = create_user
    assignee = create_assigned_user

    ticket = Ticket.objects.create(
        title="Assigned Ticket",
        description="This ticket has an assignee.",
        created_by=creator,
        assigned_to=assignee,
        status="in_progress",
    )

    assert ticket.assigned_to == assignee
    assert assignee.assigned_tickets.count() == 1
    assert creator.created_tickets.count() == 1


def test_status_choices():
    # Corrected logic to check values within the list of tuples
    choices_values = [choice[0] for choice in STATUS_CHOICES]
    assert "resolved" in choices_values
    assert "open" in choices_values


def test_priority_choices():
    # Corrected logic to check values within the list of tuples
    choices_values = [choice[0] for choice in PRIORITY_CHOICES]
    assert "high" in choices_values
    assert "medium" in choices_values
    assert "low" in choices_values


def test_ticket_update_timestamp(create_user):
    user = create_user
    ticket = Ticket.objects.create(
        title="Time Test",
        description="Testing timestamps.",
        created_by=user,
    )

    created_time = ticket.created_at
    updated_time = ticket.updated_at

    ticket.title = "Time Test Updated"
    ticket.save()
    ticket.refresh_from_db()

    assert ticket.updated_at > updated_time
    assert ticket.created_at == created_time
