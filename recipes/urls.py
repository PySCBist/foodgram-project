from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='index'),
    path('new/', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('shoppinglist/', views.shopping_list_file,
         name='shoppinglist'),
    path('purchases/', views.PurchaseListView.as_view(), name='purchases'),
    path('about/', views.AboutProjectPage.as_view(), name='about'),
    path('developer/', views.AboutAuthorPage.as_view(), name='developer'),
    path('tech/', views.AboutTechPage.as_view(), name='tech'),
    path('recipes/<slug:slug>/delete/', views.RecipeDeleteView.as_view(),
         name='delete_recipe'),
    path('recipes/<slug:slug>/edit/', views.RecipeUpdateView.as_view(),
         name='edit_recipe'),
    path('recipes/favorites/', views.FavoriteListView.as_view(),
         name='favorites'),
    path('<str:username>/', views.profile,
         name='author_page'),
    path('recipes/subscriptions/', views.subscriptions_index,
         name='subscriptions_page'),
    path('recipes/<slug:slug>/', views.RecipeDetailView.as_view(),
         name='detail_recipe'),
]
