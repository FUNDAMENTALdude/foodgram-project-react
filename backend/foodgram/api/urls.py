from django.urls import include, path
from rest_framework import routers

from .views import (TagViewSet, RecipeViewSet,
                    IngredientViewSet, CustomUserViewSet,
                    APIFollow, subscriptions,
                    APIFavorite, APIShoppingCart,
                    download_shopping_cart)


router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('users/subscriptions/', subscriptions),
    path('recipes/download_shopping_cart/', download_shopping_cart),
    path('users/<int:id>/subscribe/', APIFollow.as_view()),
    path('recipes/<int:id>/favorite/', APIFavorite.as_view()),
    path('recipes/<int:id>/shopping_cart/', APIShoppingCart.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),

]
