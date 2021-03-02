from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Ingredient, Recipe


class RecipeModelForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'time', 'description',
                  'image']

        help_texts = {'time': 'укажите время в минутах'}
        widgets = {'tags': forms.CheckboxSelectMultiple()}

    def clean(self):
        data = super().clean()
        retrieved_ingredients = []
        for key in self.data.keys():
            if 'nameIngredient' in key:
                name, id = key.split('_')
                retrieved_ingredients.append(id)

        if len(retrieved_ingredients) == 0:
            raise ValidationError(
                'В составе должен быть хотя бы один ингредиент')
        ingredients = {}
        for id in retrieved_ingredients:
            title = self.data.get(f'nameIngredient_{id}').replace("'", '"')
            amount = self.data.get(f'valueIngredient_{id}')

            if not Ingredient.objects.filter(title=title).exists():
                raise ValidationError(f'Неверный ингредиент \"{title}\",'
                                      f' пожалуйста, выберите из предложенных'
                                      )

            if int(amount) <= 0:
                raise ValidationError(
                    f'Неверное кол-во ингредиента \"{title}\"'
                )

            ingredients.update({title: amount})
        data.update({'ingredients': ingredients})
        return data
