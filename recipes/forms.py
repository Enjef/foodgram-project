from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelMultipleChoiceField

from .models import Ingredient, Recipe, Tag


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'time', 'text', 'image', 'tags', 'ingredients')

    def clean_tags(self):
        data = self.cleaned_data.get('tags')
        if not data:
            raise ValidationError('Выберите тег')
        return data

    def clean_ingredients(self):
        data = self.cleaned_data.get('recipients')
        if not data:
            raise ValidationError('Добавьте ингредиенты')
        return data
