from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils import AddRemoveMixin
from recipes.models import Favorite, Follow, Ingredient, Purchase
from users.forms import User

from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, PurchaseSerializer)


class IngredientsList(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        words = self.request.GET.get('query')
        return Ingredient.objects.filter(
            title__icontains=words).values('title', 'dimension')


class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            author_id = request.data['id']
        except KeyError:
            return Response(data='В запросе отсутствует id автора',
                            status=status.HTTP_400_BAD_REQUEST)
        author = get_object_or_404(User, pk=author_id)
        context = {"request": request}
        serializer = FollowSerializer(data={"author": author},
                                      context=context)
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data={"success": "true"}, status=status.HTTP_200_OK)

    def delete(self, request, author_id):
        author = get_object_or_404(User, pk=author_id)
        Follow.objects.filter(author=author, user=request.user.id).delete()
        return Response(data={"success": "true"}, status=status.HTTP_200_OK)


class FavoriteView(AddRemoveMixin, APIView):
    model = Favorite
    serializer_choice = FavoriteSerializer
    permission_classes = [IsAuthenticated]


class PurchaseView(AddRemoveMixin, APIView):
    model = Purchase
    serializer_choice = PurchaseSerializer
    permission_classes = [IsAuthenticated]
