from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
