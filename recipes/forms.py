from django import forms
from recipes.models import Recipe


class RecipeModelForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tag', 'time', 'description', 'image']

        help_texts = {'time': 'укажите время в минутах'}
        widgets = {'tag': forms.CheckboxSelectMultiple()}
