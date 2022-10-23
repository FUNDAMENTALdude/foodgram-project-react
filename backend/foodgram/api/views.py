from re import S, U
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action


from foodgram.settings import EXC_NAME
from users.models import User, Follow
from recipes.models import IngredientRecipe, Recipe, Tag, Ingredient, Favorite, ShoppingCart

from .filters import IngredientsSearchFilter, RecipeFilter
from .pagination import RecipePagination
from .permissions import IsAuthorAdminOrReadOnly
from .serializers import (ShoppingCartSerializer, TagSerializer, FavoriteRecipesSerializer,
                          RecipeSerializerGet, RecipeSerializerCreate,
                          IngredientSerializer, FollowSerializer,
                          SubscriptionsSerializer, FavoriteSerializer)

from djoser.views import UserViewSet





class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class CustomUserViewSet(UserViewSet):
    pagination_class = RecipePagination
    pass


class APIFollow(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        data = {'author': id, 'user': request.user.id}
        serializer = FollowSerializer(
            data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        follow = get_object_or_404(Follow, user=user, author=author, )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def subscriptions(request):

    paginator = RecipePagination()
    user = request.user
    subbed_on = Follow.objects.filter(user=user)
    result = paginator.paginate_queryset(subbed_on, request)
    serializer = SubscriptionsSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorAdminOrReadOnly]
    pagination_class = RecipePagination
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializerGet
        return RecipeSerializerCreate

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        return serializer.save()


class APIFavorite(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        data = {'recipe': id, 'user': request.user.id}
        serializer = FavoriteSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe,)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIShoppingCart(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        data = {'recipe': id, 'user': request.user.id}
        serializer = ShoppingCartSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        favorite = get_object_or_404(ShoppingCart, user=user, recipe=recipe, )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_shopping_cart(request):

    user=request.user
    ingredients = IngredientRecipe.objects.filter(
        recipe__shopping_cart__user=user
    )

    ingredients = ingredients.values(
        'ingredient__name',
        'ingredient__measurement_unit',
    ).annotate(
        amount=Sum('amount')
    )

    shopping_cart = '\n'.join([
        f'{ingredient["ingredient__name"]} '
        f'({ingredient["ingredient__measurement_unit"]}) – '
        f'{ingredient["amount"]}'
        for ingredient in ingredients
    ])

    response = FileResponse(shopping_cart, content_type='text')
    response['Content-Disposition'] = ('attachment; filename=shopping_cart.txt')

    return response
