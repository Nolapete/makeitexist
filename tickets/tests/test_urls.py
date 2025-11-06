# ruff: noqa: S101, W0621, S106
from django.urls import resolve, reverse

from tickets import views


def test_ticket_list_url_resolves():
    url = reverse("ticket_list")
    assert resolve(url).func == views.ticket_list
    assert url == "/tickets/"  # Corrected assertion


def test_create_ticket_url_resolves():
    url = reverse("create_ticket")
    assert resolve(url).func == views.create_ticket
    assert url == "/tickets/ticket/new/"  # Corrected assertion


def test_ticket_detail_url_resolves():
    url = reverse("ticket_detail", kwargs={"pk": 123})

    resolver_match = resolve(url)
    assert resolver_match.func == views.ticket_detail
    assert resolver_match.kwargs["pk"] == 123
    assert url == "/tickets/ticket/123/"  # Corrected assertion


def test_root_url_is_landing_page():  # Renamed test function
    """Test that the project root URL maps to the landing view name."""
    resolved_view = resolve("/")
    assert resolved_view.url_name == "landing"  # Corrected assertion
