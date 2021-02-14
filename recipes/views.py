from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView
from transliterate import translit
from recipes.forms import RecipeModelForm
from recipes.models import Recipe, Follow, User, Favorite, Tag
from django.contrib.auth.mixins import LoginRequiredMixin

ALL_TAGS = Tag.objects.all()


class RecipeListView(ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 6

    def tags(self):
        user_removed_tags = list(self.request.GET)
        user_removed_tags_queryset = Tag.objects.filter(
            title__in=user_removed_tags)
        tag_for_context = list(set(ALL_TAGS) - set(user_removed_tags_queryset))
        return tag_for_context

    @property
    def extra_context(self):
        active_tags = self.tags()
        if self.request.user.is_authenticated:
            favorite = Recipe.objects.filter(
                in_favorites__user=self.request.user)
            return {'favorite': favorite,
                    'active_tags': active_tags,
                    'all_tags': ALL_TAGS}

    def get_queryset(self):
        active_tags = self.tags()
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
            return {'follow': follow, 'favorite': favorite}


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
        recipe.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_recipe', kwargs={'slug': self.object.slug})


@login_required()
def subscriptions_index(request):
    # authors_list = get_list_or_404(User, following__user=request.user)
    authors_list = User.objects.filter(following__user=request.user)
    paginator = Paginator(authors_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html',
                  {'page': page, 'paginator': paginator})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    user_removed_tags = list(request.GET)
    user_removed_tags_queryset = Tag.objects.filter(
        title__in=user_removed_tags)
    tag_for_context = list(set(ALL_TAGS) - set(user_removed_tags_queryset))
    recipes_list = author.recipes.filter(
        tag__title__in=tag_for_context).order_by('-pub_date').distinct()
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_anonymous:
        follow = False
        favorite = False
    else:
        follow = Follow.objects.filter(author=author, user=request.user)
        favorite = Recipe.objects.filter(in_favorites__user=request.user)
    return render(request, 'authorRecipe.html',
                  {'recipe_list': page_obj,
                   'author': author,
                   'paginator': paginator,
                   'follow': follow,
                   'favorite': favorite,
                   'active_tags': tag_for_context,
                   'all_tags': ALL_TAGS})


class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    paginate_by = 6
    template_name = 'favorite.html'

    def tags(self):
        user_removed_tags = list(self.request.GET)
        user_removed_tags_queryset = Tag.objects.filter(
            title__in=user_removed_tags)
        tag_for_context = list(set(ALL_TAGS) - set(user_removed_tags_queryset))
        return tag_for_context

    @property
    def extra_context(self):
        active_tags = self.tags()
        favorite = Recipe.objects.filter(in_favorites__user=self.request.user)
        return {'favorite': favorite,
                'all_tags': ALL_TAGS,
                'active_tags': active_tags}

    def get_queryset(self):
        active_tags = self.tags()
        return Recipe.objects.filter(in_favorites__user=self.request.user,
                                     tag__title__in=active_tags).order_by(
            '-pub_date').distinct()


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
