from django.db import models

class Repository(models.Model):
    """Stores metadata about a GitHub repository."""
    repo_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    html_url = models.URLField()
    last_synced = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner}/{self.name}"

    class Meta:
        # We will use this to sort repositories alphabetically later
        ordering = ['name']

class Commit(models.Model):
    """Stores individual commit information."""
    sha = models.CharField(max_length=40, unique=True, primary_key=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='commits')
    message = models.TextField()
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField(max_length=254)
    date = models.DateTimeField()
    html_url = models.URLField()

    def __str__(self):
        return f"{self.sha[:7]} - {self.message[:50]}"

    class Meta:
        # Requirement: Sort chronologically descending (newest first)
        ordering = ['-date', 'repository__name']
