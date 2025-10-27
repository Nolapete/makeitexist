"""
URL configuration for makeitexist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from landing.views import landing_page

admin.site.site_header = "makeitexist.net Administration"
admin.site.site_title = "makeitexist.net"
admin.site.index_title = "Make It Exist Admin Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing_page, name="landing"),
    path("tickets/", include("tickets.urls")),
    path("pantry/", include("pantry.urls")),
    path("api/pantry/", include("pantry.api_urls")),
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # For login, logout, password management
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
