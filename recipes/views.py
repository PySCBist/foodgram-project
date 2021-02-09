from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView
from transliterate import translit
from recipes.forms import RecipeModelForm
from recipes.models import Recipe


class RecipeListView(ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 10


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'singlePage.html'


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeModelForm
    template_name = 'formRecipe.html'

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.slug = slugify(
            translit(recipe.title, language_code='ru', reversed=True))
        recipe.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_recipe', kwargs={'slug': self.object.slug})
