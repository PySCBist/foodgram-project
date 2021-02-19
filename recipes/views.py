import csv

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, \
    DeleteView, UpdateView
from transliterate import translit
from recipes.forms import RecipeModelForm
from recipes.models import Recipe, Follow, User, Favorite, Tag, Content, \
    Purchase
from django.contrib.auth.mixins import LoginRequiredMixin
from recipes.utils import adding_ingredients_to_recipe, tags

ALL_TAGS = Tag.objects.all()


class RecipeListView(ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 6

    @property
    def extra_context(self):
        active_tags = tags(self.request)
        if self.request.user.is_authenticated:
            favorite = Recipe.objects.filter(
                in_favorites__user=self.request.user)
            purchase = Recipe.objects.filter(
                purchases__user=self.request.user)
            return {'favorite': favorite,
                    'active_tags': active_tags,
                    'all_tags': ALL_TAGS,
                    'purchase': purchase
                    }

    def get_queryset(self):
        active_tags = tags(self.request)
        return Recipe.objects.filter(tag__title__in=active_tags).order_by(
            '-pub_date').distinct()


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'singlePage.html'

    @property
    def extra_context(self):
        if self.request.user.is_authenticated:
            follow = Follow.objects.filter(author=self.object.author,
                                           user=self.request.user)
            favorite = Favorite.objects.filter(recipe=self.object,
                                               user=self.request.user)
            purchase = Purchase.objects.filter(recipe=self.object,
                                               user=self.request.user)
            recipe_ingredients = Content.objects.filter(recipe=self.object)
            return {'follow': follow,
                    'favorite': favorite,
                    'recipe_ingredients': recipe_ingredients,
                    'purchase': purchase
                    }


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeModelForm
    template_name = 'formRecipe.html'

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.slug = slugify(
            translit(recipe.title, language_code='ru', reversed=True))
        n = 2
        while Recipe.objects.filter(slug=recipe.slug).exists():
            recipe.slug = recipe.slug + "_" + str(n)
            n += 1
        adding_ingredients_to_recipe(recipe, form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_recipe', kwargs={'slug': self.object.slug})


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeModelForm
    template_name = 'formRecipe.html'

    @property
    def extra_context(self):
        recipe_ingredients = Content.objects.filter(recipe=self.object)
        return {'recipe_ingredients': recipe_ingredients,
                'all_tags': ALL_TAGS}

    def get_success_url(self):
        return reverse('detail_recipe', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        recipe = form.save(commit=False)
        self.object.ingredients.clear()
        adding_ingredients_to_recipe(recipe, form)
        return super().form_valid(form)


class RecipeDeleteView(DeleteView):
    model = Recipe
    success_url = reverse_lazy('index')


class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    paginate_by = 6
    template_name = 'favorite.html'

    @property
    def extra_context(self):
        active_tags = tags(self.request)
        favorite = Recipe.objects.filter(in_favorites__user=self.request.user)
        purchase = Recipe.objects.filter(purchases__user=self.request.user)
        return {'favorite': favorite,
                'all_tags': ALL_TAGS,
                'active_tags': active_tags,
                'purchase': purchase
                }

    def get_queryset(self):
        active_tags = tags(self.request)
        return Recipe.objects.filter(in_favorites__user=self.request.user,
                                     tag__title__in=active_tags).order_by(
            '-pub_date').distinct()


class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'shopList.html'


@login_required()
def subscriptions_index(request):
    authors_list = User.objects.filter(following__user=request.user)
    paginator = Paginator(authors_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html',
                  {'page': page,
                   'paginator': paginator
                   })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    active_tags = tags(request)
    recipes_list = author.recipes.filter(
        tag__title__in=active_tags).order_by('-pub_date').distinct()
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_anonymous:
        follow, favorite, purchase = False
    else:
        follow = Follow.objects.filter(author=author, user=request.user)
        favorite = Recipe.objects.filter(in_favorites__user=request.user)
        purchase = Recipe.objects.filter(purchases__user=request.user)
    return render(request, 'authorRecipe.html',
                  {'recipe_list': page_obj,
                   'author': author,
                   'paginator': paginator,
                   'follow': follow,
                   'favorite': favorite,
                   'active_tags': active_tags,
                   'all_tags': ALL_TAGS,
                   'purchase': purchase
                   })


@login_required()
def shopping_list_file(request):
    selected_content = Content.objects.filter(
        recipe__purchases__user=request.user)
    if not selected_content:
        return redirect('index')
    ingredients = selected_content.values('ingredient').annotate(
        title=F('ingredient__title'), dimension=F('ingredient__dimension'),
        sum=Sum('amount'))

    response = HttpResponse(content_type='text/text')
    response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
    writer = csv.writer(response)
    writer.writerow([f'Ваш список покупок:'])
    writer.writerow([])
    for ingredient in ingredients:
        title = ingredient['title']
        amount = ingredient['sum']
        dimension = ingredient['dimension']
        writer.writerow([f' • {title} ({dimension}) - {amount}'])
    writer.writerow([])
    writer.writerow(['footgram - продуктовый помощник'])
    return response


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
