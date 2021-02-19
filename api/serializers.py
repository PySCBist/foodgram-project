from rest_framework import serializers

from recipes.models import Ingredient, Follow, User, Recipe, Favorite, Purchase


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = serializers.SlugRelatedField(slug_field='username',
                                          queryset=User.objects.all())

    class Meta:
        fields = ('user', 'author')
        model = Follow

    def validate(self, data):
        if data['user'] == data['author']:
            raise serializers.ValidationError(
                "Нельзя подписываться на самого себя!")
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.SlugRelatedField(slug_field='username',
                                        queryset=User.objects.all())

    class Meta:
        fields = ('recipe', 'user')
        model = Favorite


class PurchaseSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.SlugRelatedField(slug_field='username',
                                        queryset=User.objects.all())

    class Meta:
        fields = ('recipe', 'user')
        model = Purchase
