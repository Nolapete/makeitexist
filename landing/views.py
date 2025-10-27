from django.shortcuts import render
from .models import Project, StaffMember


def landing_page(request):
    makeitexist_apps = Project.objects.filter(is_makeitexist_app=True)
    external_projects = Project.objects.filter(is_makeitexist_app=False)[:4]
    staff_members = StaffMember.objects.all()  # NEW: Fetch all staff members

    context = {
        "makeitexist_apps": makeitexist_apps,
        "external_projects": external_projects,
        "staff_members": staff_members,  # NEW: Add staff members to context
    }
    return render(request, "landing/landing.html", context)
