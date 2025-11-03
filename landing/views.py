# landing/views.py
from django.shortcuts import render
from collections import defaultdict
from .models import Project, StaffMember
from github_feed.models import Commit
from django.utils import timezone


def landing_page(request):
    # ... (existing project and staff member fetching code remains the same) ...
    makeitexist_apps = Project.objects.filter(is_makeitexist_app=True)
    external_projects = Project.objects.filter(is_makeitexist_app=False)[:4]
    staff_members = StaffMember.objects.all()

    all_commits = Commit.objects.all() \
        .select_related('repository') \
        .order_by('-date')[:100]

    # NEW: Group commits by Date Object -> Repo Name -> List of Commits
    # The innermost level is a list, the others are dictionaries
    grouped_commits = defaultdict(lambda: defaultdict(list))

    for commit in all_commits:
        commit_date_object = commit.date.date()
        repo_name = commit.repository.name

        grouped_commits[commit_date_object][repo_name].append(commit)

    # Convert to standard dict and sort by date object keys (reverse for newest first)
    commits_display_data = {}
    for date_obj, repos in grouped_commits.items():
        # Sort the inner dictionary by repo name (ascending)
        sorted_repos = dict(sorted(repos.items(), key=lambda item: item[0]))
        commits_display_data[date_obj] = sorted_repos

    # Sort the outer dictionary by date keys (reverse chronological)
    sorted_commits_display_data = dict(sorted(commits_display_data.items(), reverse=True))

    context = {
        "makeitexist_apps": makeitexist_apps,
        "external_projects": external_projects,
        "staff_members": staff_members,
        # Pass the newly structured data grouped by date and repo
        "commits_by_date_and_repo": sorted_commits_display_data,
    }

    return render(request, "landing/landing.html", context)
