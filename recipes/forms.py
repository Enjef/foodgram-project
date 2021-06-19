from django.forms import ModelForm

from .models import Recipe
from .views import form_ingredients_tags


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'time', 'text', 'image',)

    def clean(self):
        self._validate_unique = True
        form_ingredients, form_tags = form_ingredients_tags(self.data)
        if not form_ingredients:
            self.add_error(None, 'Добавьте ингредиенты')
        if not form_tags:
            self.add_error(None, 'Выберите тег')
        return self.cleaned_data
