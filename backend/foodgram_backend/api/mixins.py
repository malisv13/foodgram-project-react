from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from users.models import User
from .serializers import RecipeSerializer, SubscribeAuthorSerializer


class SubscribeFavoriteShoppingCartMixin:

    @staticmethod
    def create_method(arg, model, author_or_recipe_pk, request):
        user = request.user
        if arg == Recipe:
            recipe = get_object_or_404(arg, pk=author_or_recipe_pk)
            serializer = RecipeSerializer(
                instance=recipe, context={'request': request}
            )
            if not model.objects.filter(recipe=recipe, user=user).exists():
                model.objects.create(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if arg == User:
            author = get_object_or_404(arg, pk=author_or_recipe_pk)
            serializer = SubscribeAuthorSerializer(
                instance=author, context={'request': request}
            )
            model.objects.create(user=user, author=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method(arg, model, author_or_recipe_pk, request):
        user = request.user
        if arg == Recipe:
            recipe = get_object_or_404(arg, pk=author_or_recipe_pk)
            model.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if arg == User:
            author = get_object_or_404(arg, pk=author_or_recipe_pk)
            model.objects.filter(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
