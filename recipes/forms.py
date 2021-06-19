from django.forms import ModelForm
from django.forms.models import ModelMultipleChoiceField

from .models import Recipe, Tag


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'time', 'text', 'image', 'tags', 'ingredients')

        tags = ModelMultipleChoiceField(
            queryset=Tag.objects.all()
        )
