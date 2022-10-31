from django.contrib import admin
from recipes.models import Tag, Ingredient, Favorite, ShoppingCart
from users.models import Follow


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite',)
    list_filter = ('name', 'author__username', 'tags',)
    search_fields = ('name', 'author__username', 'tags__name')

    def favorite(self, obj):
        if Favorite.objects.filter(recipe=obj).exists():
            return Favorite.objects.filter(recipe=obj).count()
        return 0


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(ShoppingCart)
