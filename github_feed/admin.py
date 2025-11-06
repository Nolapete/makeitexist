# github_feed/admin.py
from django.contrib import admin

from .models import Commit, Repository


# Optional: Customize the admin display for better readability
class CommitAdmin(admin.ModelAdmin):
    list_display = ("sha", "repository_name", "author_name", "date")
    list_filter = ("repository__name", "date")
    search_fields = ("message", "author_name", "sha")

    def repository_name(self, obj):
        return obj.repository.name

    repository_name.admin_order_field = "repository__name"


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "last_synced")
    search_fields = ("name", "owner")


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Commit, CommitAdmin)
