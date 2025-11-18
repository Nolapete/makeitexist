from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from landing.views import landing_page

admin.site.site_header = "makeitexist.net Administration"
admin.site.site_title = "makeitexist.net"
admin.site.index_title = "Make It Exist Admin Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing_page, name="landing"),
    path("blog/", include("blog.urls")),
    path("tickets/", include("tickets.urls")),
    path("pantry/", include("pantry.urls")),
    path("api/pantry/", include("pantry.api_urls")),
    path("recipes/", include("recipe.urls")),
    path("meals/", include("meals.urls")),
    path("accounts/", include("allauth.urls")),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    # Append the debug toolbar URLs to the existing list
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
