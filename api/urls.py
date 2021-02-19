from django.urls import path
from rest_framework.authtoken import views as authviews

from . import views

urlpatterns = [
    path('v1/api-token-auth/', authviews.obtain_auth_token),
    path('v1/ingredients/', views.IngredientsList.as_view(),
         name='get_ingredients'),
    path('v1/subscriptions/<int:author_id>/', views.FollowView.as_view(),
         name='remove_subscribe'),
    path('v1/subscriptions/new/', views.FollowView.as_view(),
         name='new_subscribe'),
    path('v1/favorites/add/', views.FavoriteView.as_view(),
         name='add_favorite'),
    path('v1/favorites/<int:recipe_id>/', views.FavoriteView.as_view(),
         name='remove_favorite'),
    path('v1/purchases/add/', views.PurchaseView.as_view(),
         name='add_purchase'),
    path('v1/purchases/<int:recipe_id>/', views.PurchaseView.as_view(),
         name='remove_purchase'),

]
