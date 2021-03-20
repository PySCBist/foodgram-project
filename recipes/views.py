import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView)
from foodgram.settings import PAGINATION_PAGE_SIZE

from recipes.forms import RecipeModelForm
from recipes.models import (Content, Favorite, Follow, Purchase, Recipe, Tag,
                            User)
from recipes.permissions import IsOwnerResourceOrModerator
from recipes.utils import adding_ingredients_to_recipe


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/index.html'
    paginate_by = PAGINATION_PAGE_SIZE

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['active_tags'] = list(
            Tag.objects.exclude(title__in=list(self.request.GET)))
        context['all_tags'] = Tag.objects.all()
        if self.request.user.is_authenticated:
            context['favorite'] = Recipe.objects.filter(
                in_favorites__user=self.request.user)
            context['purchase'] = Recipe.objects.filter(
                purchases__user=self.request.user)
        return context

    def get_queryset(self):
        active_tags = list(
            Tag.objects.exclude(title__in=list(self.request.GET)))
        return Recipe.objects.filter(tags__title__in=active_tags).order_by(
            '-pub_date').distinct()


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail_recipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe_ingredients'] = Content.objects.filter(
            recipe=self.object)
        if self.request.user.is_authenticated:
            context['follow'] = Follow.objects.filter(
                author=self.object.author,
                user=self.request.user)
            context['favorite'] = Favorite.objects.filter(
                recipe=self.object,
                user=self.request.user)
            context['purchase'] = Purchase.objects.filter(
                recipe=self.object,
                user=self.request.user)

        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeModelForm
    template_name = 'recipes/form_recipe.html'

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        adding_ingredients_to_recipe(recipe, form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_recipe', kwargs={'slug': self.object.slug})


class RecipeUpdateView(IsOwnerResourceOrModerator, UpdateView):
    model = Recipe
    form_class = RecipeModelForm
    template_name = 'recipes/form_recipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe_ingredients'] = Content.objects.filter(
            recipe=self.object)
        context['all_tags'] = Tag.objects.all()
        return context

    def get_success_url(self):
        return reverse('detail_recipe', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        recipe = form.save(commit=False)
        self.object.ingredients.clear()
        adding_ingredients_to_recipe(recipe, form)
        return super().form_valid(form)


class RecipeDeleteView(IsOwnerResourceOrModerator, DeleteView):
    model = Recipe
    success_url = reverse_lazy('index')


class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    paginate_by = PAGINATION_PAGE_SIZE
    template_name = 'recipes/favorite.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['favorite'] = Recipe.objects.filter(
            in_favorites__user=self.request.user)
        context['purchase'] = Recipe.objects.filter(
            purchases__user=self.request.user)
        context['active_tags'] = list(
            Tag.objects.exclude(title__in=list(self.request.GET)))
        context['all_tags'] = Tag.objects.all()
        return context

    def get_queryset(self):
        active_tags = list(
            Tag.objects.exclude(title__in=list(self.request.GET)))
        return Recipe.objects.filter(in_favorites__user=self.request.user,
                                     tags__title__in=active_tags).order_by(
            '-pub_date').distinct()


class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'recipes/purchases.html'

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)


@login_required()
def subscriptions_index(request):
    authors_list = User.objects.filter(following__user=request.user)
    paginator = Paginator(authors_list, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/my_follow.html',
                  {'page': page,
                   'paginator': paginator
                   })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    active_tags = list(Tag.objects.exclude(title__in=list(request.GET)))
    recipes_list = author.recipes.filter(
        tags__title__in=active_tags).order_by('-pub_date').distinct()
    paginator = Paginator(recipes_list, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_anonymous:
        follow = purchase = favorite = False
    else:
        follow = Follow.objects.filter(author=author, user=request.user)
        favorite = Recipe.objects.filter(in_favorites__user=request.user)
        purchase = Recipe.objects.filter(purchases__user=request.user)
    return render(request, 'recipes/author_page.html',
                  {'recipe_list': page_obj,
                   'author': author,
                   'paginator': paginator,
                   'follow': follow,
                   'favorite': favorite,
                   'active_tags': active_tags,
                   'all_tags': Tag.objects.all(),
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
    writer.writerow(['Ваш список покупок:'])
    writer.writerow([])
    for ingredient in ingredients:
        title = ingredient['title']
        amount = ingredient['sum']
        dimension = ingredient['dimension']
        writer.writerow([f' • {title} ({dimension}) - {amount}'])
    writer.writerow([])
    writer.writerow(['foodgram - продуктовый помощник'])
    return response


class AboutProjectPage(TemplateView):
    template_name = 'recipes/about_project.html'


class AboutAuthorPage(TemplateView):
    template_name = 'recipes/about_author.html'


class AboutTechPage(TemplateView):
    template_name = 'recipes/about_tech.html'
