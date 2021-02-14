from django.contrib.auth import get_user_model
from django.db import models

from recipes.validators import validate_positive_number

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Приём пищи')
    colour = models.CharField(max_length=20, verbose_name='Цвет тега')

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'colour')


class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    tag = models.ManyToManyField(Tag, verbose_name='Тег',
                                 related_name='recipes')
    time = models.PositiveSmallIntegerField(verbose_name='Время приготовления',
                                            validators=[
                                                validate_positive_number])
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    image = models.ImageField(upload_to='foodgram/', blank=True, null=True,
                              verbose_name='Загрузка изображения')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название',
                             db_index=True)
    dimension = models.CharField(max_length=20,
                                 verbose_name='Единица измерения', blank=True,
                                 null=True)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиент',
                                   related_name='ingredient')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    amount = models.PositiveSmallIntegerField(verbose_name='Колличество',
                                              validators=[
                                                  validate_positive_number])


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        unique_together = ('user', 'author')


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='in_favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='has_favorites',
                             verbose_name='Пользователь')
