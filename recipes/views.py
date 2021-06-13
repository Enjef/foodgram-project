from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from http import HTTPStatus
from recipes.models import (
    Cart, Ingredient, Recipe, RecipeIngredient, Subscription, Tag, User
)
from foodgram.settings import PAGE_SIZE_INDEX, PAGE_SIZE_CART
from .forms import RecipeForm
from django.db.models import Sum


class RecipeListView(ListView):
    context_object_name = 'recipe_list'
    queryset = Recipe.objects.all()
    paginate_by = PAGE_SIZE_INDEX
    page_title = None

    def get_queryset(self):
        tags = self.request.GET.get('tags')
        if tags is None:
            return self.queryset
        tags = tags.split(',')
        tags = Tag.objects.filter(slug__in=tags)
        recipes = self.queryset.filter(tags__in=tags)
        return recipes

    def get_context_data(self, **kwargs):
        kwargs.update({'page_title': self._get_page_title()})
        tags = Tag.objects.all()
        kwargs.update({'tags_all': tags})
        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
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
    paginate_by = PAGE_SIZE_CART
    queryset = Cart.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(customer=self.request.user)
        return qs


def form_ingredients_tags(request):
    form_ingredients = {}
    form_tags = []
    ing_part = []
    ing_keys = ['nameIngred', 'valueIngre', 'unitsIngre']
    for field in request:
        if field in ['breakfast', 'lunch', 'dinner']:
            form_tags.append(get_object_or_404(Tag, slug=field).id)
            continue
        if field[:10] not in ing_keys:
            continue
        ing_part.append(request[field])
        if len(ing_part) != 3:
            continue
        title = ing_part[0]
        amount = float(ing_part[1].replace(',', '.'))
        dimention = ing_part[2]
        if title in form_ingredients:
            form_ingredients[title][1] += amount
        else:
            ing = get_object_or_404(
                Ingredient,
                title=title,
                dimension=dimention
            )
            if ing:
                form_ingredients[title] = [ing, amount]
        ing_part = []

    return list(form_ingredients.values()), form_tags


def recipe_ingredient_bulk_create(form_ingredients, recipe):
    objects = []
    for ingredient in form_ingredients:
        objects.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient[0],
                amount=ingredient[1])
        )
    RecipeIngredient.objects.bulk_create(objects)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    page_title = 'Создание рецепта'
    form_class = RecipeForm
    template_name = 'recipes/formRecipe.html'

    def form_valid(self, form):
        form_ingredients, form_tags = form_ingredients_tags(self.request.POST)
        if not form_tags or not form_ingredients:
            return super().form_invalid(form)
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        form.save()
        self.object.tags.add(*form_tags)
        recipe_ingredient_bulk_create(form_ingredients, self.object)
        form.save_m2m()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        tags = Tag.objects.all()
        kwargs.update({'tags_all': tags})
        context = super().get_context_data(**kwargs)
        return context


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = 'index'


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    page_title = 'Создание рецепта'
    form_class = RecipeForm
    template_name = 'recipes/formChangeRecipe.html'

    def get_context_data(self, **kwargs):
        tags = Tag.objects.all()
        kwargs.update({'tags_all': tags})
        context = super().get_context_data(**kwargs)
        return context

    def get_initial(self):
        initial = super().get_initial()
        tags = list(Tag.objects.filter(recipes=self.object))
        initial['tags'] = tags
        initial['recipe_ingredients'] = RecipeIngredient.objects.filter(
            recipe=self.object
        )
        initial['slug'] = self.object.slug
        return initial

    def form_valid(self, form):
        form_ingredients, form_tags = form_ingredients_tags(self.request.POST)
        if not form_tags or not form_ingredients:
            return super().form_invalid(form)
        self.object = form.save(commit=False)
        self.object.tags.set([])
        recipeingredients = RecipeIngredient.objects.filter(recipe=self.object)
        if recipeingredients:
            recipeingredients.delete()
        form_image = self.request.POST.get('image')
        if form_image:
            self.object.image = 'recipes/images/' + form_image
        form.save()
        self.object.tags.add(*form_tags)
        recipe_ingredient_bulk_create(form_ingredients, self.object)
        return super().form_valid(form)


def shoping_list_view(request):
    carts = Cart.objects.filter(customer=request.user)
    recipes = Recipe.objects.filter(in_cart__in=carts)
    recipes_ingredients = RecipeIngredient.objects.filter(
        recipe__in=recipes
    )

    ingredients = (
        recipes_ingredients.values('ingredient_title').annotate(
            total_amount=Sum('amount')
        )
    )
    out = str(ingredients)
    '''for item in ingredients:
        out.append(' '.join([item, str(ingredients[item]) + '\n']))
    out = ''.join(sorted(out))'''
    filename = 'my_shoping_list.txt'
    response = HttpResponse(out, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=HTTPStatus.NOT_FOUND
    )


def server_error(request):
    return render(
        request,
        'misc/auth.html',
        status=HTTPStatus.INTERNAL_SERVER_ERROR
    )


def about(request):
    return render(request, 'misc/about.html', status=HTTPStatus.OK)


def tech(request):
    return render(request, 'misc/tech.html', status=HTTPStatus.OK)
