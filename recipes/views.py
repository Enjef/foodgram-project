from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from recipes.models import (Cart, Ingredient, Recipe, RecipeIngredient,
                            Subscription, Tag, User)

from .forms import RecipeForm


class RecipeListView(ListView):
    context_object_name = 'recipe_list'
    queryset = Recipe.objects.all()
    paginate_by = 6
    page_title = None

    def get_queryset(self):
        tags = self.request.GET.get('tags')
        print(self.request.GET)
        if tags is None:
            return self.queryset
        tags = tags.split(',')
        tags = Tag.objects.filter(slug__in=tags)
        recipes = self.queryset.filter(tags__in=tags)
        return recipes

    def get_context_data(self, **kwargs):
        kwargs.update({'page_title': self._get_page_title()})
        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        assert self.page_title, ('Attribute "page_title" not set '
                                 'for {self.__class__.__name__}')
        return self.page_title


class IndexListView(RecipeListView):
    page_title = 'Рецепты'
    template_name = 'recipes/index.html'


class FavoriteListView(LoginRequiredMixin, RecipeListView):
    page_title = 'Избранное'
    template_name = 'recipes/index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(following__user=self.request.user)
        return qs


class ProfileView(RecipeListView):
    context_object_name = 'profile_list'
    template_name = 'recipes/authorRecipe.html'

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs.get('username'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Recipe.objects.filter(author=self.user)
        tags = self.request.GET.get('tags', None)
        if tags is None:
            return qs
        tags = tags.split(',')
        tags = Tag.objects.filter(slug__in=tags)
        qs = qs.filter(tags__in=tags)
        return qs

    def _get_page_title(self):
        return self.user.get_full_name() or self.user.username

    def get_context_data(self, **kwargs):
        kwargs.update({
            'page_title': self._get_page_title(),
            'author': self.user})
        context = super().get_context_data(**kwargs)
        return context


class RecipeDetailView(DetailView):
    queryset = Recipe.objects.all()
    template_name = 'recipes/singlePage.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs
            .prefetch_related('recipe_ingredients__ingredient')
        )
        return qs


class SubscriptionListView(LoginRequiredMixin, RecipeListView):
    context_object_name = 'subscription_list'
    template_name = 'recipes/myFollow.html'
    page_title = 'Мои подписки'
    queryset = Subscription.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class CartListView(LoginRequiredMixin, RecipeListView):
    context_object_name = 'cart_list'
    template_name = 'recipes/shopList.html'
    page_title = 'Список покупок'
    paginate_by = 15
    queryset = Cart.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(customer=self.request.user)
        return qs


def form_ingredients_tags(request):
    #  отсутствующие в базе отбрасываются, дубликаты суммируются
    form_ingredients = {}
    form_tags = []
    ing_part = []
    ing_keys = ['nameIngred', 'valueIngre', 'unitsIngre']
    for field in request:
        if field[:10] in ing_keys:
            ing_part.append(request[field])
            if len(ing_part) == 3:
                title = ing_part[0]
                amount = float(ing_part[1].replace(',', '.'))
                dimention = ing_part[2]
                if title in form_ingredients:
                    form_ingredients[title][1] += amount
                else:
                    ing = Ingredient.objects.filter(
                        title=title,
                        dimension=dimention
                    )
                    if ing.exists():
                        form_ingredients[title] = [ing, amount]
                ing_part = []
        if field in ['breakfast', 'lunch', 'dinner']:
            form_tags.append(get_object_or_404(Tag, slug=field).id)
    return list(form_ingredients.values()), form_tags


def recipe_ingredient_bulk_create(form_ingredients, recipe):
    objects = []
    for ingredient in form_ingredients:
        objects.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient[0][0],
                amount=ingredient[1])
        )
    RecipeIngredient.objects.bulk_create(objects)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    page_title = 'Создание рецепта'
    form_class = RecipeForm
    template_name = 'recipes/formRecipe.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        form_ingredients, form_tags = form_ingredients_tags(self.request.POST)
        if not form_tags or not form_ingredients:
            return super().form_invalid(form)
        form.save()
        self.object.tags.add(*form_tags)
        recipe_ingredient_bulk_create(form_ingredients, self.object)
        form.save_m2m()
        return super().form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = '/'


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    page_title = 'Создание рецепта'
    form_class = RecipeForm
    template_name = 'recipes/formChangeRecipe.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['tags'] = [
            tag.name for tag in Tag.objects.filter(recipes=self.object)
        ]
        initial['recipe_ingredients'] = RecipeIngredient.objects.filter(
            recipe=self.object
        )
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.tags.set([])
        RecipeIngredient.objects.filter(recipe=self.object).delete()
        form_image = self.request.POST.get('image')
        if form_image:
            self.object.image = 'recipes/images/' + form_image
        form_ingredients, form_tags = form_ingredients_tags(self.request.POST)
        if not form_tags or not form_ingredients:
            return super().form_invalid(form)
        form.save()
        self.object.tags.add(*form_tags)
        recipe_ingredient_bulk_create(form_ingredients, self.object)
        return super().form_valid(form)


def shoping_list_view(request):
    carts = Cart.objects.filter(customer=request.user)
    recipes = Recipe.objects.filter(in_cart__in=carts)
    recipes_intgredients = RecipeIngredient.objects.filter(
        recipe__in=recipes
    )
    ingredients = {}
    for recipe_ingr in recipes_intgredients:
        if recipe_ingr.ingredient.title in ingredients:
            ingredients[recipe_ingr.ingredient.title][0] += (
                recipe_ingr.amount
            )
        else:
            ingredients[recipe_ingr.ingredient.title] = [
                recipe_ingr.amount, recipe_ingr.ingredient.dimension
            ]
    out = []
    for item in ingredients:
        out.append(' '.join([
            item,
            str(ingredients[item][0]),
            ingredients[item][1]]) + '\n'
        )
    out = ''.join(sorted(out))
    filename = "my_shoping_list.txt"
    response = HttpResponse(out, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/auth.html', status=500)


def about(request):
    return render(request, 'misc/about.html', status=200)


def tech(request):
    return render(request, 'misc/tech.html', status=200)
