from django.urls import path

from . import views

app_name = "recipe"


urlpatterns = [
    path("add/", views.add_recipe, name="add_recipe"),
    path("", views.list_recipes, name="list_recipes"),
    path("update/<int:recipe_id>/", views.update_recipe, name="update_recipe"),
    path("delete/<int:recipe_id>/", views.delete_recipe, name="delete_recipe"),
    path("search", views.search_recipes, name="search_recipes"),
]
