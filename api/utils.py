from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.models import Recipe


class AddRemoveMixin:
    serializer_choice = None
    model = None

    def post(self, request):
        try:
            recipe_id = request.data['id']
        except KeyError:
            return Response(data='В запросе отсутствует id рецепта',
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_choice(
            data={"recipe": recipe_id, "user": self.request.user})
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data={"success": "true"}, status=status.HTTP_200_OK)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        self.model.objects.filter(recipe=recipe,
                                  user=request.user.id).delete()
        return Response(data={"success": "true"}, status=status.HTTP_200_OK)
