## Quick orientation for AI coding agents

This repository is a Django monolith (Django 5.x) with several apps and integrations. Below are concise, actionable pointers so an AI agent can be productive immediately.

### Big picture
- Django project root: `manage.py` with settings at `config/settings.py`.
- Major apps: `blog`, `github_feed`, `landing`, `meals`, `pantry`, `recipe`, `tickets`.
- E-commerce platform: uses Django Oscar (many `oscar.*` apps are in `INSTALLED_APPS`) — keep Oscar app ordering in mind when touching `INSTALLED_APPS`.
- Background jobs: Celery is configured (see `config/celery.py` and `CELERY_*` in `config/settings.py`). A periodic task `github_feed.tasks.sync_all_github_data` runs hourly.
- Search: Haystack with Whoosh backend is used (`HAYSTACK_CONNECTIONS` and `WHOOSH_INDEX_PATH`).

### Key conventions & patterns
- Secrets/config: `django-environ` reads a `.env` adjacent to `BASE_DIR` (see `config/settings.py`). Don't hardcode secrets—use `env("VAR_NAME")`.
- Authentication: site-wide login requirement via `config.middleware.LoginRequiredMiddleware`. Exceptions are listed in `LOGIN_REQUIRED_EXEMPT_URLS` (e.g., `^accounts/.*`, `^api/.*`). API endpoints default to `IsAuthenticated` (see `REST_FRAMEWORK` setting).
- Tests: pytests are used. `pytest.ini` sets `DJANGO_SETTINGS_MODULE = config.settings`. Test files follow `test_*.py`, `*_tests.py`, or `tests.py` patterns.
- Fixtures: app-level fixtures live under `*/fixtures/` (example: `blog/fixtures/initial_*.json`). Use them in tests via `pytest` fixtures or `loaddata`.
- Migrations: apps include migration files under `*/migrations/`. Avoid editing historic migration files unless necessary.

### Developer workflows (how to run things locally)
- Use the `ndm.sh` wrapper to run Django management commands within the Nix development environment: `./ndm.sh runserver` or `./ndm.sh migrate` (it runs `nix develop --command .venv/bin/python manage.py "$@"`).
- Run tests with pytest inside the dev environment: `nix develop --command .venv/bin/python -m pytest` (pytest respects `pytest.ini`).
- Start Celery worker from project root (inside the project's venv/Nix dev): `celery -A config worker -l info` and scheduler `celery -A config beat -l info` if needed.

### Deployment & CI
- Deployment workflow calls a remote script via `.github/workflows/deploy.yml` and SSHs to a Linode server to run `project_manager.sh makeitexist deploy`. Keep secrets in GitHub Actions secrets.

### Code patterns to follow when editing
- When adding REST endpoints, honor project-wide auth: default to `IsAuthenticated` and explicitly set `AllowAny` for public endpoints.
- When adding periodic tasks or Celery tasks, register them under app `tasks.py` and add schedule entries in `config/settings.py` if periodic.
- Keep templates under `templates/` and app-specific templates under `app_name/templates/`. Templates use Django templates and `django-htmx` is present for interactivity.

### Files to check when making changes
- `config/settings.py` (global configuration)
- `config/celery.py` (celery app config)
- `manage.py` (entrypoint)
- `ndm.sh` (how to run manage.py in Nix dev)
- `pytest.ini` (pytest config)
- `pyproject.toml` and `requirements.txt` (dependencies; `pyproject.toml` pins many dev tools)
- `blog/fixtures/*` and `*/migrations/*` for data and schema changes

### Quick examples
- Add an API view that is public (example skeleton): set permission_classes = [AllowAny] and register path under `api_urls.py` or the app's `urls.py`.
- To add a scheduled Celery beat job: implement `tasks.py` in the app and add a schedule entry to `CELERY_BEAT_SCHEDULE` in `config/settings.py` (see existing `sync-github-every-hour` example).

If anything here is unclear or you want me to include more concrete code snippets (for example, a Celery task skeleton or how to run full test suite in Nix), tell me which area to expand and I will iterate.
