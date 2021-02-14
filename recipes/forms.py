from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe, Ingredient


class RecipeModelForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tag', 'time', 'description', 'image']

        help_texts = {'time': 'укажите время в минутах'}
        widgets = {'tag': forms.CheckboxSelectMultiple()}

    def clean(self):
        print(self.data.keys())
        data = super().clean()
        print(data)
        retrieved_ingredients = []
        for key in self.data.keys():
            if 'nameIngredient' in key:
                name, id = key.split('_')
                retrieved_ingredients.append(id)

        for id in retrieved_ingredients:
            title = self.data.get(f'nameIngredient_{id}')
            amount = self.data.get(f'valueIngredient_{id}')

            if int(amount) == 0:
                raise ValidationError(
                    f'Неверное кол-во ингредиента \'{title}\'')

            if Ingredient.objects.filter(title=title).exists():
                print('da', f'{title}', f'{amount}')

            else:
                raise ValidationError(
                    f'Неверный ингредиент \'{title}\', пожалуйста, '
                    f'выберите из предложенных')

        return data

