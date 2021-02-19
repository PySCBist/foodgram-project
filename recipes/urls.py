from django.urls import path

from recipes import views as v

urlpatterns = [
    path('', v.RecipeListView.as_view(), name='index'),
    path('new/', v.RecipeCreateView.as_view(), name='create_recipe'),
    path('shoppinglist/', v.shopping_list_file,
         name='shoppinglist'),
    path('purchases/', v.PurchaseListView.as_view(), name='purchases'),
    path('about/', v.AboutProjectPage.as_view(), name='about'),
    path('developer/', v.AboutAuthorPage.as_view(), name='developer'),
    path('tech/', v.AboutTechPage.as_view(), name='tech'),
    path('recipes/<str:slug>/delete/', v.RecipeDeleteView.as_view(),
         name='delete_recipe'),
    path('recipes/<str:slug>/edit/', v.RecipeUpdateView.as_view(),
         name='edit_recipe'),
    path('recipes/favorites/', v.FavoriteListView.as_view(), name='favorites'),
    path('<str:username>/', v.profile,
         name='author_page'),
    path('recipes/subscriptions/', v.subscriptions_index,
         name='subscriptions_page'),
    path('recipes/<slug:slug>/', v.RecipeDetailView.as_view(),
         name='detail_recipe'),
]
