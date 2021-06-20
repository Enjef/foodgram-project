from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe, Tag


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


def form_ingredients_tags(request):
    form_ingredients = {}
    form_tags = []
    ing_part = []
    tag_keys = Tag.objects.values_list('slug', flat=True)
    all_ingredients = Ingredient.objects.values_list('title', flat=True)
    ing_keys = ['nameIngred', 'valueIngre', 'unitsIngre']
    for field in request:
        if field in tag_keys:
            form_tags.append(get_object_or_404(Tag, slug=field).id)
            continue
        if field[:10] not in ing_keys:
            continue
        ing_part.append(request[field])
        if len(ing_part) != 3:
            continue
        title = ing_part[0]
        if title not in all_ingredients:
            ing_part = []
            continue
        amount = float(ing_part[1].replace(',', '.'))
        dimension = ing_part[2]
        if title in form_ingredients:
            form_ingredients[title][1] += amount
        else:
            ing = get_object_or_404(
                Ingredient,
                title=title,
                dimension=dimension
            )
            form_ingredients[title] = [ing, amount]
        ing_part = []

    return list(form_ingredients.values()), form_tags
