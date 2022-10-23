from django.db import models
from django.db.models import UniqueConstraint
from users.models import User
from django.core.validators import MinValueValidator, RegexValidator
from foodgram.settings import MINIMUM_AMOUNT_OF_INGREDIENT
from foodgram.settings import MINIMUM_COOKING_TIME


class Tag(models.Model):

    name = models.CharField(
        max_length=32,
        verbose_name='name',
        help_text='Название тега',
        unique=True,
    )

    color = models.CharField(
        max_length=7,
        unique=True,
        validators=(
            RegexValidator(
                regex='#[0-9A-Fa-f]{6}',
                message='Color must be in HEX format',
            ),
        )
    )

    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
        max_length=15,
    )

    class Meta:
        ordering = ['name',]
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):

    name = models.CharField(
        verbose_name='name',
        max_length=100,
        unique=True,
    )

    measurement_unit = models.CharField(
        verbose_name='measurement_unit',
        max_length=20,
    )

    class Meta:
        ordering = ['name',]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return self.name

class Recipe(models.Model):

    name = models.CharField(max_length=40)

    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='теги'
    )

    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        related_name='recipes',                 
        verbose_name='Ингредиенты',
        through='IngredientRecipe'
    )

    image = models.ImageField(
        upload_to='images/',
        null=True, default=None, blank=True
    )

    text = models.TextField(
        verbose_name='Описание'
    )

    cooking_time = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1, message='минимум 1')],
        verbose_name='Время готовности'
    )

    date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):

    ingredient = models.ForeignKey(
        Ingredient,                     
        related_name='ingredient',
        on_delete=models.PROTECT
    )
    recipe = models.ForeignKey(Recipe, related_name='recipe',
                               on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1, message='минимум 1')]
    )

    class Meta:
        ordering = ['ingredient']
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return (
            f'{self.recipe}  {self.ingredient},'
            f'количество = {self.amount}'
        )

class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite',
        verbose_name='Пользователь',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite',
        verbose_name='Рецепт',
    )

    class Meta:

        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipes_in_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'