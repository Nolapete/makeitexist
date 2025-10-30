from django.db import models
from django.core.validators import RegexValidator


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.CharField(
        max_length=200, help_text="e.g., Python, Django, PostgreSQL"
    )
    tech_icons = models.CharField(
        max_length=500,
        blank=True,
        help_text="Font Awesome icon classes, separated by commas (e.g., 'fab fa-python, fab fa-django').",
    )
    image = models.ImageField(upload_to="project_images/")
    project_url = models.URLField(
        blank=True, help_text="The URL to the project's website."
    )
    is_makeitexist_app = models.BooleanField(
        default=True, help_text="Is this an app for config.net?"
    )
    display_domain = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="The domain name to display (e.g., clownfishgenetics.org)",
    )
    is_featured = models.BooleanField(
        default=False, help_text="Mark this project as featured."
    )

    def __str__(self):
        return self.title

    def get_tech_icons(self):
        """Returns a list of icon classes."""
        return [icon.strip() for icon in self.tech_icons.split(",") if icon.strip()]


# NEW: Staff Member Model
class StaffMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    photo = models.ImageField(upload_to="staff_photos/", blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name
