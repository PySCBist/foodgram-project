from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest

from recipes.models import Content, Ingredient


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
