from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField

from .models import Ingredient, Recipe, Tag


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'time', 'text', 'image', 'tags', 'ingredients')

        tags = ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
        ingredients = ModelMultipleChoiceField(
            queryset=Ingredient.objects.all()
        )
