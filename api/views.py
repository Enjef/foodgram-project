from recipes.models import Cart, Favorite, Ingredient, Subscription
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import IngredientSerializer


class FavoritesView(APIView):
    def post(self, request, format=None):
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data.get('id')
        )
        return Response({'success': True}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        favorite = get_object_or_404(
            Favorite,
            recipe_id=pk,
            user=request.user
        )
        favorite.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class PurchasesView(APIView):
    def post(self, request, format=None):
        Cart.objects.get_or_create(
            customer=request.user,
            recipe_id=request.data.get('id')
        )
        return Response({'success': True}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        cart_obj = get_object_or_404(Cart, recipe_id=pk, customer=request.user)
        cart_obj.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class SubscriptionsView(APIView):
    def post(self, request, format=None):
        Subscription.objects.get_or_create(
            user=request.user,
            author_id=request.data.get('id')
        )
        return Response({'success': True}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        sub_obj = get_object_or_404(Subscription, author=pk, user=request.user)
        sub_obj.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class IngredientsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        key_word = self.request.GET.get('query', '')
        if key_word is not None:
            queryset = queryset.filter(title__istartswith=key_word[:-1])
        return queryset
