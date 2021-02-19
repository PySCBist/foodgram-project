from django.contrib import admin
from .models import Recipe, Tag, Ingredient, Favorite, Follow, Content, \
    Purchase


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'time', 'description', 'author', 'slug', 'pub_date',)
    search_fields = ('title',)
    list_filter = ('pub_date',)
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'colour',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user',)
    list_filter = ('recipe',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user',)
    list_filter = ('user',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'user',)
    list_filter = ('user', 'author',)


class ContentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
    list_filter = ('recipe',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Purchase, PurchaseAdmin)
