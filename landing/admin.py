from django.contrib import admin

from .models import Project, StaffMember


# Re-using existing ProjectAdmin class
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_makeitexist_app",
        "is_featured",
        "project_url",
        "display_domain",
    )
    list_filter = ("is_makeitexist_app", "is_featured")
    search_fields = ("title", "description", "display_domain")


# NEW: StaffMemberAdmin class
@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email")
