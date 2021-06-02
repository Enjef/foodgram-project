from recipes.models import Cart, Favorite, Ingredient, Subscription
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import IngredientSerializer


class FavoritesView(APIView):
    def post(self, request, format=None):
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id']
        )
        return Response({'success': True}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        Favorite.objects.filter(recipe_id=pk, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)

    @classmethod
    def get_extra_actions(cls):
        return []


class PurchasesView(APIView):
    def get(self, request, format=None):
        purchases = [
            purchase for purchase in Cart.objects.filter(customer=request.user)
        ]
        return Response(purchases)

    def post(self, request, format=None):
        Cart.objects.get_or_create(
            customer=request.user,
            recipe_id=request.data['id']
        )
        return Response({'success': True}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        Cart.objects.filter(recipe_id=pk, customer=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)

    @classmethod
    def get_extra_actions(cls):
        return []


class SubscriptionsView(APIView):
    def post(self, request, format=None):
        Subscription.objects.get_or_create(
            user=request.user,
            author_id=request.data['id']
        )
        return Response({'success': True}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        Subscription.objects.filter(author=pk, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)

    @classmethod
    def get_extra_actions(cls):
        return []


class IngredientsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        key_word = self.request.GET.get('query', '')
        if key_word is not None:
            queryset = queryset.filter(title__istartswith=key_word[:-1])
        return queryset
