# blog/views.py
import markdown
from django.shortcuts import get_object_or_404, render
from django.utils.html import strip_tags  # Import this helper

from .models import Post

MD_EXTENSIONS = ["fenced_code"]


def post_list(request):
    posts = Post.objects.filter(is_published=True)

    for post in posts:
        # 1. Convert full content markdown to HTML
        full_html_content = markdown.markdown(post.content, extensions=MD_EXTENSIONS)
        # 2. Strip HTML tags to get plain text
        plain_text_content = strip_tags(full_html_content)
        # 3. Truncate the plain text cleanly
        truncated_text = " ".join(plain_text_content.split()[:50]) + "..."
        # 4. Store plain text summary temporarily on the object
        post.summary = truncated_text

    context = {"posts": posts}
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)

    # Process the FULL content field for the detail view
    html_content = markdown.markdown(post.content, extensions=MD_EXTENSIONS)

    context = {
        "post": post,
        "html_content": html_content,  # Pass the new HTML content
    }
    return render(request, "blog/post_detail.html", context)
