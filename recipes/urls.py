from django.urls import path

from recipes.views import (CartListView, FavoriteListView, IndexListView,
                           ProfileView, RecipeCreateView, RecipeDeleteView,
                           RecipeDetailView, RecipeUpdateView,
                           SubscriptionListView, shoping_list_view)

urlpatterns = [
    path('recipes/<slug:slug>/', RecipeDetailView.as_view(), name='recipe'),
    path('edit/<slug:slug>/', RecipeUpdateView.as_view(), name='edit'),
    path(
        'subscriptions/',
        SubscriptionListView.as_view(),
        name='subscriptions'
    ),
    path('create/', RecipeCreateView.as_view(), name='create'),
    path('delete/<slug:slug>/', RecipeDeleteView.as_view(), name='delete'),
    path('purchases/', CartListView.as_view(), name='purchases'),
    path('favorites/', FavoriteListView.as_view(), name='favorites'),
    path('profiles/<str:username>/', ProfileView.as_view(), name='profile'),
    path('shoping_txt/', shoping_list_view, name='shoping_list_txt'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('', IndexListView.as_view(), name='index')]
