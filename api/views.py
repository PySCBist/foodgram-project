from api.utils import AddRemoveMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Ingredient, Follow, Favorite, Purchase
from rest_framework import generics, status

from users.forms import User
from .serializers import IngredientSerializer, FollowSerializer, \
    FavoriteSerializer, PurchaseSerializer


class IngredientsList(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        words = self.request.GET.get('query')
        return Ingredient.objects.filter(
            title__icontains=words).values('title', 'dimension')


class FollowView(APIView):
    def post(self, request):
        author_id = request.data['id']
        author = User.objects.get(pk=author_id)
        context = {"request": request}
        serializer = FollowSerializer(data={"author": author},
                                      context=context)
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data={"success": "true"}, status=status.HTTP_200_OK)

    def delete(self, request, author_id):
        Follow.objects.filter(author=author_id, user=request.user.id).delete()
        return Response(data={"success": "true"}, status=status.HTTP_200_OK)


class FavoriteView(AddRemoveMixin, APIView):
    model = Favorite
    serializer_choice = FavoriteSerializer


class PurchaseView(AddRemoveMixin, APIView):
    model = Purchase
    serializer_choice = PurchaseSerializer
