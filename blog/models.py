# blog/models.py
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField()

    # The excerpt field allows for a manual summary, optional.
    excerpt = models.TextField(blank=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # This helps link to individual posts easily
        return reverse("blog:post_detail", kwargs={"slug": self.slug})
