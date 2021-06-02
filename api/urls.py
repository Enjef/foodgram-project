from django.urls import path

from api.views import (FavoritesView, IngredientsViewSet, PurchasesView,
                       SubscriptionsView)

urlpatterns = [
    path('purchases/', PurchasesView.as_view(), name='purchase'),
    path('purchases/<int:pk>/', PurchasesView.as_view(), name='purchase'),
    path('subscriptions/', SubscriptionsView.as_view(), name='subscription'),
    path(
        'subscriptions/<int:pk>/',
        SubscriptionsView.as_view(),
        name='subscription'
    ),
    path('favorites/', FavoritesView.as_view(), name='favorite'),
    path('favorites/<int:pk>/', FavoritesView.as_view(), name='favorite'),
    path(
        'ingredients/',
        IngredientsViewSet.as_view({'get': 'list'}),
        name='ingredient'
    ),
]
