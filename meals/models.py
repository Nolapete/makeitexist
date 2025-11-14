from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    last_chosen = models.DateField(null=True, blank=True)
    ingredients = models.ManyToManyField("Ingredient", related_name="recipes")

    def __str__(self):
        return self.title


class MealLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    chosen_date = models.DateField(default=models.DateField(auto_now_add=True))

    def __str__(self):
        return f"{self.recipe.title} chosen on {self.chosen_date}"


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
