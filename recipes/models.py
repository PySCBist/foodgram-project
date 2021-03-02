from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from transliterate import translit

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Приём пищи')
    colour = models.CharField(max_length=20, verbose_name='Цвет тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = [models.UniqueConstraint(fields=['title', 'colour'],
                                               name='unique_tag')]

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название',
                             db_index=True)
    dimension = models.CharField(max_length=20,
                                 verbose_name='Единица измерения', blank=True,
                                 null=True)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название',
                             blank=False)
    slug = models.SlugField(unique=True, verbose_name='URL')
    tags = models.ManyToManyField(Tag, verbose_name='Тег',
                                  related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, through='Content',
                                         verbose_name='Ингредиенты',
                                         related_name='recipes')
    time = models.PositiveSmallIntegerField(verbose_name='Время приготовления')
    description = models.TextField(blank=False,
                                   verbose_name='Описание')
    image = models.ImageField(upload_to='foodgram/', blank=True, null=True,
                              verbose_name='Загрузка изображения')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Recipe, self).save(*args, **kwargs)
        if not self.slug:
            slug = slugify(
                translit(self.title, language_code='ru', reversed=True))
            if Recipe.objects.filter(slug=slug).exists():
                self.slug = "%s-%s" % (slug, self.id)
            else:
                self.slug = slug
            self.save()


class Content(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиент',
                                   related_name='ingredient')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='content_recipe')
    amount = models.PositiveSmallIntegerField(verbose_name='Колличество')

    class Meta:
        verbose_name = 'Состав'
        verbose_name_plural = 'Состав рецептов'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following', verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                                               name='unique_follow')]


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='in_favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='has_favorites',
                             verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='purchases',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='purchases',
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_purchase')]
