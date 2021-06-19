from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'time', 'text', 'image',)

    def clean(self):
        self._validate_unique = True
        form_ingredients = self.data.get('nameIngred')
        form_tags = self.data.get('tags')
        if not form_ingredients:
            self.add_error(None, 'Добавьте ингредиенты')
        if not form_tags:
            self.add_error(None, 'Выберите тег')
        return self.cleaned_data
