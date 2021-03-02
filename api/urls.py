from django.urls import include, path
from rest_framework.authtoken import views as authviews

from . import views

urls = [
    path('api-token-auth/', authviews.obtain_auth_token, name='get_token'),
    path('ingredients/', views.IngredientsList.as_view(),
         name='get_ingredients'),
    path('subscriptions/<int:author_id>/', views.FollowView.as_view(),
         name='remove_subscribe'),
    path('subscriptions/new/', views.FollowView.as_view(),
         name='new_subscribe'),
    path('favorites/add/', views.FavoriteView.as_view(),
         name='add_favorite'),
    path('favorites/<int:recipe_id>/', views.FavoriteView.as_view(),
         name='remove_favorite'),
    path('purchases/add/', views.PurchaseView.as_view(),
         name='add_purchase'),
    path('purchases/<int:recipe_id>/', views.PurchaseView.as_view(),
         name='remove_purchase'),
]

urlpatterns = [
    path('v1/', include(urls)),
]
