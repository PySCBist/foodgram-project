from django.urls import path

from recipes import views as v

urlpatterns = [
    path('', v.RecipeListView.as_view(), name='index'),
    path('new/', v.RecipeCreateView.as_view(), name='create_recipe'),
    path('recipes/favorites/', v.FavoriteListView.as_view(), name='favorites'),
    path('<str:username>/', v.profile,
         name='author_page'),
    path('recipes/subscriptions/', v.subscriptions_index,
         name='subscriptions_page'),
    path('recipes/<slug:slug>/', v.RecipeDetailView.as_view(),
         name='detail_recipe'),
]
