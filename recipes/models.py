import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    dimension = models.CharField(max_length=128, verbose_name='ед. измерения')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Инргедиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.title} {self.dimension}'


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Тег'
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Слаг',
        default=uuid.uuid1
    )
    style = models.CharField(
        max_length=200,
        verbose_name='Стиль'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    title = models.CharField(max_length=256, verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=False,
        verbose_name='Картинка',
        help_text='Загрузите изображение'
    )
    text = models.TextField(verbose_name='Текстовое описание',)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    time = models.PositiveIntegerField(
        verbose_name='Время приготовления (мин)',
        validators=[MinValueValidator(1)]
    )
    slug = models.SlugField(unique=True, max_length=256, default=uuid.uuid1,)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return f'{self.title} от {self.author}'

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'slug': self.slug})


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient_recipes'
    )
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self) -> str:
        return (f'{self.ingredient.title} {self.amount} '
                f'{self.ingredient.dimension} в {self.recipe}'
                )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            ),
        )
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self) -> str:
        return f'Избранное {self.user}: {self.recipe}'


class Cart(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer',
        verbose_name='Покупатель',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='in_cart',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('customer', 'recipe',),
                name='unique_сart'
            ),
        )
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self) -> str:
        return f'Корзина {self.customer}: {self.recipe}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_follow'
            ),
        )
        ordering = ('-author',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'Подписка юзера {self.user} на {self.author}'

    def clean(self):
        if self.user == self.author:
            from django.core.exceptions import ValidationError
            raise ValidationError('Нельзя подписаться на себя')
