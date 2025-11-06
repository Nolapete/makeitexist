# ruff: noqa: S101, W0621, S106
# config/tests/test_root_urls.py

from django.conf import settings
from django.urls import URLResolver, get_resolver, resolve, reverse

from config import urls  # Direct import of the urls module


def test_admin_url_exists():
    admin_url = reverse("admin:index")
    assert admin_url == "/admin/"
    resolved_func = resolve(admin_url).func
    assert "AdminSite" in str(resolved_func)


def test_landing_page_root_url():
    url = reverse("landing")
    assert url == "/"
    resolved_view = resolve(url)
    assert "landing_page" in str(resolved_view.func)


def test_tickets_app_urls_included():
    """Test that the tickets app URLs are included correctly."""
    url = reverse("ticket_list")
    assert url == "/tickets/"

    # Check the actual urls.urlpatterns list directly
    found = False
    for pattern in urls.urlpatterns:
        if isinstance(pattern, URLResolver) and str(
            getattr(pattern, "pattern", pattern)
        ).startswith("tickets/"):
            found = True
            break
    assert found is True


def test_pantry_app_urls_included():
    # Placeholder until you provide pantry URLs
    pass


def test_auth_urls_included():
    url = reverse("login")
    assert url == "/accounts/login/"


def test_static_media_urls_in_debug_mode():
    """
    Verify that static and media URLs are NOT added to urlpatterns
    when DEBUG is False (which is the case during testing).
    """
    # Use get_resolver as requested in the prompt
    resolver = get_resolver(settings.ROOT_URLCONF)
    urlpatterns = resolver.url_patterns

    found_media_pattern = False
    for pattern in urlpatterns:
        # Use the new pattern string extraction logic:
        # str(getattr(pattern, "pattern", pattern))
        pattern_string = str(getattr(pattern, "pattern", pattern))
        if "media/" in pattern_string:
            found_media_pattern = True
            break

    # Because DEBUG is False during testing, this should be False
    assert found_media_pattern is False
