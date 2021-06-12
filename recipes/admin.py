from django.contrib import admin
from django.contrib.admin.decorators import register
from django.db.models.aggregates import Count

from recipes.models import (
    Cart, Favorite, Ingredient, Recipe, RecipeIngredient, Subscription, Tag
)


@register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)
    empty_value_display = '-пусто-'
    search_fields = (
        'title',
    )
    list_filter = (
        'title',
    )


@register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    fields = (
        'ingredient',
        'recipe',
        'amount',
    )
    search_fields = (
        'ingredient',
        'recipe',
    )


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'slug',
        'style',
    )
    search_fields = (
        'name',
    )


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'recipe_follower_count',)
    readonly_fields = ('recipe_follower_count',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(recipe_follower_count=Count('following'))
        return qs

    def recipe_follower_count(self, obj):
        return obj.recipe_follower_count
    recipe_follower_count.short_description = 'Добавлений в избранное'

    fields = (
        'author',
        'title',
        'image',
        'text',
        'tags',
        'time',
        'slug',
        'recipe_follower_count',
    )
    search_fields = (
        'title',
        'author__username',
    )
    list_filter = (
        'title',
        'author__username',
        'tags',
    )
    autocomplete_fields = (
        'ingredients',
    )
    inlines = (
        RecipeIngredientInline,
    )


@register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'recipe',
    )
    search_fields = (
        'user__username',
    )


@register(Cart)
class CartAdmin(admin.ModelAdmin):
    fields = (
        'customer',
        'recipe',
    )
    search_fields = (
        'customer__username',
    )


@register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    empty_value_display = '-пусто-'
    search_fields = (
        'author',
    )
    list_filter = (
        'author',
    )
