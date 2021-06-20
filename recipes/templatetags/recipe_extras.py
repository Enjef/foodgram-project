import django_filters
from recipes.models import Recipe, Tag
from django import template

register = template.Library()


class RecipeFilter(django_filters.FilterSet):
    class Meta:
        model = Recipe
        fields = ('tags', 'author',)


@register.filter
def is_favorite(recipe, user):
    return recipe.following.filter(user=user).exists()


@register.filter
def in_cart(recipe, user):
    return recipe.in_cart.filter(customer=user).exists()


@register.filter
def in_subs(author, user):
    return author.author.filter(user=user).exists()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.simple_tag
def my_url(value, field_name, urlencode=None):
    url = f'?{field_name}={value}'
    if urlencode:
        querystring = urlencode.split('&')
        filterset_querystring = [
            part for part in querystring if part.split('=')[0] != field_name
        ]
        encoded_querystring = '&'.join(filterset_querystring)
        if encoded_querystring:
            url = f'{url}&{encoded_querystring}'
    return url


@register.simple_tag
def my_tag(value, field_name, path, urlencode=None):
    if not urlencode:
        url = f'?{field_name}={value}'
        return url
    filtered_querystring = []
    tags_all = Tag.objects.values_list('slug', flat=True)
    for tag in tags_all:
        if tag in urlencode:
            filtered_querystring.append(tag)
    if value in urlencode and value in filtered_querystring:
        filtered_querystring.pop(filtered_querystring.index(value))
    else:
        filtered_querystring.append(value)
    if not filtered_querystring:
        return f'{path}'
    encoded_querystring = ','.join(filtered_querystring)
    url = f'?{field_name}={encoded_querystring}'
    return url


@register.simple_tag
def declension(qty):
    if 4 < qty % 100 < 20 or qty % 10 in [0, 5, 6, 7, 8, 9]:
        return 'рецептов...'
    if 1 < qty % 10 < 5:
        return 'рецепта...'
    else:
        return 'рецепт...'


@register.filter
def subtract(cur, prev):
    return cur - prev
