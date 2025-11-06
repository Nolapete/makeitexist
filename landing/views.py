# landing/views.py
from collections import defaultdict

from django.shortcuts import render

from blog.models import Post  # Import the Post model
from github_feed.models import Commit

from .models import Project, StaffMember


def landing_page(request):
    makeitexist_apps = Project.objects.filter(is_makeitexist_app=True)
    external_projects = Project.objects.filter(is_makeitexist_app=False)[:4]
    staff_members = StaffMember.objects.all()

    all_commits = (
        Commit.objects.all().select_related("repository").order_by("-date")[:100]
    )

    # Group commits by Date Object -> Repo Name -> List of Commits
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
    sorted_commits_display_data = dict(
        sorted(commits_display_data.items(), reverse=True)
    )

    # --- NEW: Fetch Highlight Data ---
    latest_blog_post = (
        Post.objects.filter(is_published=True).order_by("-pub_date").first()
    )
    latest_project = Project.objects.order_by(
        "-id"
    ).first()  # Assuming higher ID is newer
    # The latest commit is just the first one in your already-fetched list
    latest_commit = all_commits.first()

    context = {
        "makeitexist_apps": makeitexist_apps,
        "external_projects": external_projects,
        "staff_members": staff_members,
        # Pass the newly structured data grouped by date and repo
        "commits_by_date_and_repo": sorted_commits_display_data,
        # Add the highlight items to the context
        "latest_blog_post": latest_blog_post,
        "latest_project": latest_project,
        "latest_commit": latest_commit,
    }

    return render(request, "landing/landing.html", context)
