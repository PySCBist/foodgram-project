from django.urls import path
from .views import RecipeListView, RecipeDetailView, RecipeCreateView

urlpatterns = [
    path('', RecipeListView.as_view(), name='index'),
    path('recipes/<slug:slug>/', RecipeDetailView.as_view(),
         name='detail_recipe'),
    path('new/', RecipeCreateView.as_view(), name='create_recipe'),
]
