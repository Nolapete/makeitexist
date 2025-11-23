# Zencoder Rules for Make It Exist - Django Project

## Project Overview
Make It Exist Studios is a comprehensive Django 5.2.6 web application with e-commerce (Django Oscar), meal planning, recipes, pantry management, ticketing, blog, GitHub feed integration, and CRM functionality.

## Key Apps & Structure
- **landing** - Landing/public pages
- **meals** - Meal planning with Recipe, Ingredient, MealLog models
- **pantry** - Inventory management with alerts
- **tickets** - Support ticketing system
- **blog** - Blog publishing
- **recipe** - Recipe management
- **github_feed** - GitHub data synchronization (Celery task every hour)
- **Django Oscar** - Full e-commerce platform

## Code Conventions

### Python & Django Standards
- Python 3.12+
- Line length: 88 characters (Ruff enforced)
- Quote style: Double quotes (Ruff enforced)
- Format: Black / Ruff formatter
- Linting: Ruff with rules E, W, F, I, UP, B, C4, DJ, S
- Pre-commit hooks: Required for linting/formatting

### Django Patterns
- Use Django ORM with PostgreSQL
- Models: Define in `models.py`, use descriptive field names
- Views: Class-based views preferred (CreateView, UpdateView, DetailView)
- Forms: Define in `forms.py`, use Django forms or ModelForms
- URLs: Namespace apps in `urls.py`
- Templates: Use base.html inheritance from `templates/base.html`
- Admin: Register models in `admin.py` with custom admin classes

### Project Structure
```
app_name/
├── migrations/          # Auto-generated, never edit
├── templates/
│   └── app_name/
│       ├── list.html
│       ├── detail.html
│       ├── form.html
│       └── ...
├── static/
│   └── app_name/
├── models.py           # Database models
├── views.py            # Views (CBV preferred)
├── forms.py            # Forms
├── urls.py             # URL routing
├── admin.py            # Admin interface
├── apps.py             # App config
├── tests.py            # Tests (pytest + pytest-django)
└── __init__.py
```

### Database Patterns
- Use PostgreSQL (`DATABASE_URL` env var)
- Run migrations: `python manage.py makemigrations && python manage.py migrate`
- Avoid editing migration files manually
- Use descriptive model field names
- Add related_name to ForeignKey/ManyToMany relationships
- Use blank=True, null=True carefully (avoid null on CharField)

### Async Tasks (Celery)
- Redis broker: `redis://localhost:6379/0`
- Task location: `app_name/tasks.py`
- Define tasks with `@shared_task` decorator
- Use Celery Beat for scheduling (configured in settings.py)
- Example: GitHub feed syncs hourly via `github_feed.tasks.sync_all_github_data`

### Authentication & Permissions
- Use Django-allauth for user auth (Google, GitHub OAuth)
- Login required by default: `@login_required` decorator
- Exempt URLs in settings: `/accounts/*`, `/api/*`, `/static/*`, `/media/*`
- Check permissions in views: `permission_required`, `user_passes_test`

### API Development
- Use Django Ninja for API endpoints (`api_urls.py`, `api_views.py`)
- REST Framework for compatibility
- API auth: Default to `IsAuthenticated` permission
- Endpoints should be namespaced under `/api/`

### Search & Indexing
- Use Haystack + Whoosh for full-text search
- Signal processor: RealtimeSignalProcessor (auto-indexes on model changes)
- Index path: `{BASE_DIR}/whoosh_index/`

### Testing
- Framework: Pytest + pytest-django
- Config: `pytest.ini`
- Test files: `tests.py` in each app or `tests/` directory
- Run tests: `pytest` or `pytest tests/test_sanity_checks.py`
- Use pytest fixtures for common setup

### Deployment
- Uses GitHub Actions: `.github/workflows/deploy.yml`
- Collect static files: `python manage.py collectstatic`
- Run migrations in deployment
- Environment: PostgreSQL, Redis, Gunicorn/ASGI
- Requires: SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS env vars

## Security Best Practices
- Never commit `.env` files or secrets
- Use `django-environ` for configuration
- CSRF protection: Enabled by default
- SQL Injection: Protected by Django ORM
- XSS: Template auto-escaping enabled
- Secure cookies: SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE in production
- SSL redirect: SECURE_SSL_REDIRECT in production

## Common Tasks

### Adding a New Feature
1. Create models in `app/models.py`
2. Create forms in `app/forms.py` if needed
3. Create views in `app/views.py`
4. Create templates in `app/templates/app/`
5. Add URLs in `app/urls.py` and root `config/urls.py`
6. Create tests in `app/tests.py`
7. Run migrations: `python manage.py makemigrations && python manage.py migrate`
8. Test locally
9. Run lint/format: `ruff format . && ruff check .`
10. Commit and push

### Debugging
- Use Django Debug Toolbar (enabled in DEBUG mode)
- Check logs: `python manage.py runserver` output
- Database: Django shell: `python manage.py shell`
- Templates: Add print() or use Django template debugging

### Performance Optimization
- Use `.select_related()` for ForeignKey/OneToOne
- Use `.prefetch_related()` for ManyToMany/reverse ForeignKey
- Cache with Redis
- Index frequently queried fields
- Use pagination for large querysets

## Dependencies
- Django 5.2.6
- PostgreSQL (psycopg2-binary)
- Redis
- Celery
- Django Oscar
- Django-allauth
- Django Haystack + Whoosh
- Ruff, Black, Flake8
- Pytest, pytest-django

## Environment Variables
- `SECRET_KEY` - Django secret key (required)
- `DEBUG` - Boolean, default False
- `DATABASE_URL` - PostgreSQL connection
- `GITHUB_PAT` - GitHub Personal Access Token
- `GITHUB_USERNAME` - GitHub username
- `ALLOWED_HOSTS` - Comma-separated hosts
- `EMAIL_BACKEND` - Email configuration
