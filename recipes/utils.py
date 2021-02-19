from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest

from recipes.models import Ingredient, Content, Tag


def adding_ingredients_to_recipe(recipe, form):
    input_ingredients = form.cleaned_data.get('ingredients')
    try:
        with transaction.atomic():
            recipe.save()
            ingredients_for_recipe = []
            for key in input_ingredients.keys():
                ingredients_for_recipe.append(
                    Content(ingredient=Ingredient.objects.get(title=key),
                            amount=input_ingredients[key], recipe=recipe))
            Content.objects.bulk_create(ingredients_for_recipe)

        form.save_m2m()
        return recipe

    except IntegrityError:
        return HttpResponseBadRequest


def tags(request):
    all_tags = Tag.objects.all()
    user_removed_tags = list(request.GET)
    user_removed_tags_queryset = Tag.objects.filter(
        title__in=user_removed_tags)
    tag_for_context = list(set(all_tags) - set(user_removed_tags_queryset))
    return tag_for_context
