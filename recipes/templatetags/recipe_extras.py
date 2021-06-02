import django_filters
from recipes.models import Recipe
from django import template

register = template.Library()


class RecipeFilter(django_filters.FilterSet):
    class Meta:
        model = Recipe
        fields = ['tags', 'author']


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
def my_tag(value, field_name, urlencode=None):
    if not urlencode:
        url = f'?{field_name}={value}'
        return url
    filtered_querystring = []
    if 'breakfast' in urlencode:
        filtered_querystring.append('breakfast')
    if 'lunch' in urlencode:
        filtered_querystring.append('lunch')
    if 'dinner' in urlencode:
        filtered_querystring.append('dinner')
    if value in urlencode and value in filtered_querystring:
        filtered_querystring.pop(filtered_querystring.index(value))
    else:
        filtered_querystring.append(value)
    if not filtered_querystring:
        return '/'
    encoded_querystring = ','.join(filtered_querystring)
    url = f'?{field_name}={encoded_querystring}'
    return url
