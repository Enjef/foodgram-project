from django.urls import path

from api.views import (
    FavoritesView, IngredientsViewSet, PurchasesView, SubscriptionsView
)

urlpatterns = [
    path('v1/purchases/', PurchasesView.as_view(), name='purchase'),
    path('v1/purchases/<int:pk>/', PurchasesView.as_view(), name='purchase'),
    path(
        'v1/subscriptions/',
        SubscriptionsView.as_view(),
        name='subscription'
    ),
    path(
        'v1/subscriptions/<int:pk>/',
        SubscriptionsView.as_view(),
        name='subscription'
    ),
    path('v1/favorites/', FavoritesView.as_view(), name='favorite'),
    path('v1/favorites/<int:pk>/', FavoritesView.as_view(), name='favorite'),
    path(
        'v1/ingredients/',
        IngredientsViewSet.as_view({'get': 'list'}),
        name='ingredient'
    ),
]
