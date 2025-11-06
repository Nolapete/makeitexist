# github_feed/tasks.py

import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from requests.exceptions import RequestException

from .models import Commit, Repository

# Base URL for the GitHub API
BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {settings.GITHUB_PAT}",
    "Accept": "application/vnd.github.v3+json",
}
REQUEST_TIMEOUT = 10
# Define the username from settings
GITHUB_USER = settings.GITHUB_USERNAME


def fetch_paginated_data(url):
    """
    Helper function to handle GitHub API pagination automatically.
    """
    results = []
    while url:
        try:
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()  # Raise an exception for bad status codes
            results.extend(response.json())

            # Check for the 'Link' header to find the next page URL
            if "link" in response.headers:
                links = response.headers["link"].split(",")
                url = None
                for link in links:
                    if 'rel="next"' in link:
                        url = link.split(";")[0].strip("<>").strip()
                        break
            else:
                url = None
        except RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            break
        # Optional: Add a small delay to respect rate limits if needed
        # time.sleep(0.5)
    return results


@shared_task
def sync_all_github_data():
    """
    Main task to orchestrate syncing all repositories and their commits.
    """
    print(f"Starting GitHub sync for user: {GITHUB_USER}")

    repos_url = f"{BASE_URL}/users/{GITHUB_USER}/repos?type=owner&per_page=100"
    repositories_data = fetch_paginated_data(repos_url)

    if not repositories_data:
        print("No repositories found or error occurred.")
        return

    for repo_data in repositories_data:
        # Create or update the Repository model instance
        repo_instance, created = Repository.objects.update_or_create(
            repo_id=repo_data["id"],
            defaults={
                "name": repo_data["name"],
                "owner": repo_data["owner"]["login"],
                "html_url": repo_data["html_url"],
            },
        )
        # Call a sub-task or function to fetch commits for this specific repo
        fetch_commits_for_repo.delay(repo_instance.repo_id, repo_data["commits_url"])

    print("Repository sync initiated. Commit fetching tasks queued.")


@shared_task
def fetch_commits_for_repo(repo_id, commits_url):
    """
    Fetches all commits for a specific repository instance.
    """
    try:
        repo_instance = Repository.objects.get(repo_id=repo_id)
    except Repository.DoesNotExist:
        print(f"Repository with id {repo_id} not found.")
        return

    print(f"Fetching commits for {repo_instance.name}...")

    # The commits_url template needs the SHA parameter removed for listing
    api_url = commits_url.replace("{/sha}", "") + "?per_page=100"

    commits_data = fetch_paginated_data(api_url)

    new_commits_count = 0
    for commit_data in commits_data:
        commit_sha = commit_data["sha"]

        # Use update_or_create to avoid duplicates and handle updates
        # If the commit already exists, it will do nothing (since we
        # only care about new ones)
        if not Commit.objects.filter(sha=commit_sha).exists():
            # Safely get author name/email, as some commits might be missing user data
            author_info = commit_data["commit"]["author"]

            Commit.objects.create(
                sha=commit_sha,
                repository=repo_instance,
                message=commit_data["commit"]["message"],
                author_name=author_info.get("name", "Unknown"),
                author_email=author_info.get("email", "unknown@example.com"),
                date=author_info.get("date"),
                html_url=commit_data["html_url"],
            )
            new_commits_count += 1

    # Update the last synced timestamp for the repository
    repo_instance.last_synced = timezone.now()
    repo_instance.save()

    print(
        f"Finished syncing {repo_instance.name}. Added {new_commits_count} new commits."
    )
