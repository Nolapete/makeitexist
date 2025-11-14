from django.contrib import admin

from .models import Ingredient, MealLog, Recipe

admin.site.register(Recipe)
admin.site.register(MealLog)
admin.site.register(Ingredient)
