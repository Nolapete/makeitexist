from django import forms

from .models import Ingredient, Recipe


class RecipeForm(forms.ModelForm):
    """
    Form for creating and updating Recipe instances.
    The ingredients field is a ManyToManyField, which is automatically handled by
    ModelForm using a ModelMultipleChoiceField.
    """

    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all().order_by("name"),
        required=False,
    )

    class Meta:
        model = Recipe
        fields = ["title", "description", "instructions", "ingredients"]
