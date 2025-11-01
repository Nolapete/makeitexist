# config/test_settings.py

from django.conf import settings
import os

# These tests will run using the configuration loaded by pytest.ini
# By default, during testing, DEBUG will be False if not explicitly set to True.

def test_debug_setting():
    """Ensure DEBUG is False when running tests (default for Django test env)."""
    assert settings.DEBUG is False

def test_secret_key_is_loaded():
    """Ensure the SECRET_KEY is loaded from the environment and is not empty."""
    assert settings.SECRET_KEY is not None
    assert settings.SECRET_KEY != ''
    # Optional: ensure it's not the default insecure key used during project creation
    # assert 'django-insecure-' not in settings.SECRET_KEY


def test_allowed_hosts_configured():
    """Ensure ALLOWED_HOSTS is not empty in the test environment (as DEBUG is False)."""
    # django-environ sets a default of [] if the .env var is missing
    # In a proper test/prod env, this list should not be empty.
    assert len(settings.ALLOWED_HOSTS) > 0


def test_app_configurations():
    """Ensure all expected apps are installed."""
    expected_apps = ["landing", "tickets", "pantry", "rest_framework"]
    for app in expected_apps:
        assert app in settings.INSTALLED_APPS

# --- Static/Media Files Best Practices ---

def test_static_url_and_root():
    """Verify static file configuration best practices."""
    assert settings.STATIC_URL == "/static/"
    # Check that STATIC_ROOT is defined and is an absolute path
    assert settings.STATIC_ROOT is not None
    assert os.path.isabs(settings.STATIC_ROOT)
    # Check that STATICFILES_DIRS is a list and contains an absolute path
    assert isinstance(settings.STATICFILES_DIRS, list)
    assert len(settings.STATICFILES_DIRS) > 0
    assert os.path.isabs(settings.STATICFILES_DIRS[0])


def test_media_url_and_root():
    """Verify media file configuration best practices."""
    assert settings.MEDIA_URL == "/media/"
    # Check that MEDIA_ROOT is defined and is an absolute path
    assert settings.MEDIA_ROOT is not None
    assert os.path.isabs(settings.MEDIA_ROOT)


def test_production_security_settings():
    """
    Ensure production security settings are applied when DEBUG is False.
    These are the settings inside your 'if not DEBUG:' block.
    """
    assert settings.SECURE_SSL_REDIRECT is True
    assert settings.SESSION_COOKIE_SECURE is True
    assert settings.CSRF_COOKIE_SECURE is True
