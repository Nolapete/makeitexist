# Make It Exist - Repository Documentation

## Project Overview

**Make It Exist** is a comprehensive Django-based web application for the Make It Exist Studios platform. The project integrates multiple functional modules including meal planning, recipe management, ticketing, pantry management, blog capabilities, and GitHub feed integration. It also features e-commerce functionality via Django Oscar and full user authentication through Django-allauth.

**Project Name:** makeitexist  
**Version:** 0.1.0  
**Python Version:** >=3.12  
**Framework:** Django 5.2.6

---

## Technology Stack

### Core Framework
- **Django 5.2.6** - Web framework
- **Django Ninja** - API framework
- **Django REST Framework** - REST API support
- **Django Oscar** - E-commerce platform

### Authentication & User Management
- **Django-allauth** (>=65.13.0) - User authentication with social login support
  - Google OAuth
  - GitHub OAuth
- **JWT** - Token-based authentication

### Database & Caching
- **PostgreSQL** - Primary database (via psycopg2-binary)
- **Redis** - Caching and message broker
- **Celery** - Asynchronous task queue
- **Django-celery-results** - Store task results in database

### Search & Indexing
- **Django Haystack** - Search API abstraction
- **Whoosh** - Full-text search engine
- **Elasticsearch** compatible (via Haystack)

### Frontend & Templating
- **Django Templates** - Server-side templating
- **Django HTMX** - AJAX interactions
- **Sorl Thumbnail** - Image processing and thumbnails
- **Widget Tweaks** - Template filters for forms
- **BeautifulSoup4** - HTML/XML parsing

### Content Management & Tools
- **Django CRM** - Customer relationship management
- **Django Waffle** - Feature flag management
- **Django Filter** - Query filtering
- **Django Debug Toolbar** - Development debugging
- **Treebeard** - Tree data structure for hierarchical data
- **Django Tables2** - Table rendering

### Development Tools
- **Ruff** (>=0.14.5) - Python linter and formatter
- **Black** - Code formatter
- **Flake8** - Style guide enforcement
- **Pre-commit** - Git hooks framework
- **Pytest** - Testing framework
- **Pytest-Django** - Django testing utilities
- **djLint** - Django template linter

### AI & LLM Integration
- **Aider Chat** (0.86.1) - AI-assisted code development
- **Anthropic SDK** - Claude API support
- **OpenAI SDK** - GPT integration
- **LiteLLM** - LLM provider abstraction
- **Google Generative AI** - Gemini API support

### Media & File Handling
- **Pillow** - Image processing
- **pydub** - Audio processing
- **soundfile** & **sounddevice** - Audio file handling

### Utilities
- **Pydantic** - Data validation
- **YAML** - Configuration files
- **Markdown** - Markdown processing
- **Requests** - HTTP client
- **GitPython** - Git repository interaction
- **Python-decouple** - Environment configuration
- **Django-environ** - Environment variable management

---

## Project Structure

```
makeitexist/
├── config/                  # Django project settings
│   ├── settings.py         # Main settings (Django 5.2.6, Oscar, Celery)
│   ├── urls.py             # URL routing configuration
│   ├── wsgi.py             # WSGI application
│   ├── asgi.py             # ASGI application
│   └── celery.py           # Celery configuration
├── blog/                    # Blog app
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── migrations/
│   ├── templates/
│   └── tests.py
├── github_feed/            # GitHub data feed integration
│   ├── models.py
│   ├── views.py
│   ├── tasks.py            # Celery tasks for GitHub sync
│   ├── admin.py
│   ├── migrations/
│   └── tests.py
├── landing/                # Landing page app
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── migrations/
│   ├── templates/
│   └── tests.py
├── meals/                  # Meal planning & suggestions app
│   ├── models.py           # Recipe, Ingredient, MealLog
│   ├── views.py            # Meal management views
│   ├── forms.py            # Recipe & ingredient forms
│   ├── admin.py
│   ├── migrations/
│   ├── templates/
│   ├── README.md           # Meals app-specific documentation
│   └── tests.py
├── pantry/                 # Pantry inventory management
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── alerts.py           # Inventory alerts
│   ├── api_views.py        # API endpoints
│   ├── api_urls.py
│   ├── admin.py
│   ├── migrations/
│   ├── templates/
│   └── tests.py
├── recipe/                 # Recipe management app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── migrations/
│   ├── templates/
│   └── tests.py
├── tickets/                # Ticketing/support system
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   └── tests.py
├── templates/              # Global templates
│   └── base.html          # Base template
├── static/                 # Static assets
│   ├── css/
│   ├── images/
│   └── favicon.ico
├── media/                  # User-uploaded content
│   ├── project_images/
│   └── staff_photos/
├── tests/                  # Project-wide tests
│   └── test_sanity_checks.py
├── .github/                # GitHub configuration
│   └── workflows/
├── nix/                    # Nix environment configuration
│   └── requirements-deps.nix
├── manage.py               # Django CLI
├── pyproject.toml          # Python project configuration & dependencies
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Pip dependencies
├── flake.nix              # Nix development environment
├── flake.lock             # Nix lock file
├── .envrc                 # Direnv configuration
├── .pre-commit-config.yaml # Pre-commit hooks
├── .gitignore             # Git ignore patterns
├── .gitattributes         # Git attributes
└── whoosh_index/          # Full-text search index

### Data Fixtures
- blog_data.json           # Blog data fixtures
- landing.yaml             # Landing page configuration
- pantry.yaml              # Pantry test data
- testland.yaml            # Landing page test data
- testpantry.yaml          # Pantry test data
- testtickets.yaml         # Tickets test data
- db_dump.yaml             # Database backup/fixture
```

---

## Key Applications

### 1. **Meals App** 
Comprehensive meal planning and recipe management system.
- **Models:** Recipe, Ingredient, MealLog
- **Features:** 
  - Recipe CRUD operations with ingredient management
  - Dynamic meal suggestions (algorithm prioritizes recipes not chosen in 30 days)
  - Meal logging with date tracking
  - Dual-listbox ingredient selector (JavaScript-powered)
  - User authentication required
- **Views:** `add_recipe`, `edit_recipe`, `recipe_detail`, `my_recipes`, `choose_meal`

### 2. **Pantry App**
Inventory management and tracking system.
- **Features:**
  - Inventory alerts
  - Admin dashboard with 9+ admin pages
  - API endpoints for programmatic access
  - Integration with Django Oscar

### 3. **Tickets App**
Support/ticketing system.
- **Features:**
  - Ticket creation and management
  - Status tracking
  - User support interface

### 4. **GitHub Feed App**
Automated GitHub data synchronization.
- **Features:**
  - Celery task: `sync_all_github_data` (runs hourly)
  - Requires: `GITHUB_PAT` and `GITHUB_USERNAME` environment variables
  - Automatic scheduling via Celery Beat

### 5. **Blog App**
Blog publishing platform.
- **Features:**
  - Blog post management
  - Admin interface

### 6. **Landing App**
Landing page and public-facing content.
- **Features:**
  - Public landing page
  - CRM integration

### 7. **Recipe App**
Recipe management system (separate from meals app).
- **Features:**
  - Recipe CRUD
  - Form-based recipe management

---

## Configuration & Settings

### Django Settings (`config/settings.py`)
- **Database:** PostgreSQL (via `env.db()`)
- **Email Backend:** Configurable (default: console backend)
- **Authentication:** 
  - Django auth + Django-allauth
  - Google & GitHub OAuth support
- **Search:** Whoosh full-text search with Haystack
- **Security:**
  - SSL redirect enabled in production
  - CSRF protection
  - Secure session/cookie settings
- **E-commerce:** Django Oscar with shop name "Make It Exist Studios"

### Installed Apps
**Django Core:**
- admin, auth, contenttypes, sessions, messages, staticfiles, flatpages, sites

**Third-Party:**
- rest_framework, ninja, django_htmx, allauth, waffle, oscar (full suite)

**Custom Apps:**
- landing, tickets, pantry, github_feed, blog, recipe, meals

### URL Configuration
- **Root:** `config.urls`
- **Admin:** `/admin/`
- **API:** `/api/`
- **Auth:** `/accounts/` (allauth)
- **Oscar Dashboard:** `/dashboard/`
- **Search:** Haystack endpoints via oscar

### Authentication
- **Exempt Routes:**
  - `/accounts/*` - Allauth authentication flows
  - `/admin/login/` - Admin login
  - `/static/*` - Static assets
  - `/media/*` - Media files
  - `/api/*` - API (permission classes handle auth)
- **Default:** All other routes require authentication

---

## Database

### Models Overview
- **Django Oscar Models:** Comprehensive e-commerce data (products, orders, baskets, etc.)
- **Blog:** Blog posts and content
- **Meals:** Recipes, ingredients, meal logs with user relationships
- **Pantry:** Inventory tracking
- **Tickets:** Support tickets
- **GitHub Feed:** GitHub repository data
- **CRM:** Customer relationship data

### Migrations
- Located in each app's `migrations/` directory
- Automatically generated via `python manage.py makemigrations`
- Applied via `python manage.py migrate`

---

## Async Tasks (Celery)

### Configuration
- **Broker:** Redis (localhost:6379/0)
- **Result Backend:** Redis (localhost:6379/0)
- **Serializer:** JSON
- **Timezone:** UTC

### Scheduled Tasks
- **`sync_all_github_data`** (github_feed.tasks)
  - **Schedule:** Every 1 hour
  - **Purpose:** Synchronize GitHub data

### Running Celery
```bash
# Start Celery worker
celery -A config worker -l info

# Start Celery Beat (scheduler)
celery -A config beat -l info
```

---

## Search & Indexing

### Haystack Configuration
- **Engine:** Whoosh (full-text search)
- **Index Path:** `{BASE_DIR}/whoosh_index/`
- **Signal Processor:** RealtimeSignalProcessor (auto-index on model changes)

### Searching
- Oscar provides search form in template context
- Search results integrated with product catalog

---

## Development & Testing

### Testing
- **Framework:** Pytest with pytest-django
- **Configuration:** `pytest.ini`
- **Test Location:** `tests/` directory and `tests.py` in each app
- **Sanity Checks:** `tests/test_sanity_checks.py`

### Linting & Formatting
- **Linter:** Ruff (with rules: E, W, F, I, UP, B, C4, DJ, S)
- **Formatter:** Black/Ruff formatter
- **Line Length:** 88 characters
- **Exclusions:** Migration files
- **Pre-commit Hooks:** `.pre-commit-config.yaml`

### Running Commands
```bash
# Tests
pytest
pytest tests/test_sanity_checks.py

# Linting
ruff check .

# Formatting
ruff format .
black .

# Template linting
djlint templates/

# Django management
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## Environment Variables

Required in `.env` file:
- `SECRET_KEY` - Django secret key (required)
- `DEBUG` - Debug mode (bool, default: False)
- `DATABASE_URL` - PostgreSQL connection string
- `GITHUB_PAT` - GitHub Personal Access Token (for github_feed)
- `GITHUB_USERNAME` - GitHub username (for github_feed)
- `ALLOWED_HOSTS` - Comma-separated allowed hosts
- `SITE_ID` - Django site ID (default: 1)
- `EMAIL_BACKEND` - Email backend (default: console)
- `DEFAULT_FROM_EMAIL` - Default email sender

---

## Deployment

### Static Files
```bash
python manage.py collectstatic
```

### WSGI Application
- Entry point: `config.wsgi.application`
- Suitable for production deployment (Gunicorn, uWSGI, etc.)

### ASGI Application
- Entry point: `config.asgi.application`
- For async support

### Production Checklist
- Set `DEBUG = False`
- Enable SSL redirect (`SECURE_SSL_REDIRECT = True`)
- Secure session and CSRF cookies
- Use strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Set up PostgreSQL
- Configure Redis for Celery
- Run migrations
- Collect static files
- Set up proper email backend

---

## Key Dependencies & Versions

### Framework & Core
- Django 5.2.6
- django-ninja >= 1.5.0
- djangorestframework 3.16.1

### Authentication
- django-allauth >= 65.13.0
- PyJWT >= 1.4.0

### E-Commerce
- django-oscar >= 4.1
- sorl-thumbnail >= 12.11.0

### Search
- django-haystack >= 3.3
- whoosh >= 2.7.4

### Async
- celery 5.5.3
- django-celery-results >= 2.6.0
- redis 7.0.1

### AI/LLM
- anthropic 0.72.0
- openai 1.99.1
- google-generativeai 0.8.5
- aider-chat 0.86.1

### Development
- pytest 8.4.2
- pytest-django 4.11.1
- ruff >= 0.14.5
- black 25.9.0
- flake8 7.3.0
- pre-commit >= 4.4.0

---

## Notes & Best Practices

1. **Database:** Uses PostgreSQL in production; SQLite migrations are excluded from version control
2. **Search:** Whoosh index is regenerated automatically via RealtimeSignalProcessor
3. **Media:** User-uploaded files served from `/media/` directory
4. **Static Files:** Collected to `staticfiles/` during deployment
5. **Nix Support:** Project includes `flake.nix` for reproducible development environment
6. **Pre-commit:** Hooks configured to lint and format code automatically
7. **GitHub Integration:** Requires valid PAT for github_feed functionality
8. **Redis Required:** Essential for Celery task queue and caching

---

## Additional Resources

- **Django Docs:** https://docs.djangoproject.com/
- **Django Oscar:** https://django-oscar.readthedocs.io/
- **Celery Docs:** https://docs.celeryproject.org/
- **Haystack Docs:** https://django-haystack.readthedocs.io/
- **Django-allauth:** https://django-allauth.readthedocs.io/
