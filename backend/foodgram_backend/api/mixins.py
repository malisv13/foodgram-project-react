from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from users.models import User
from .serializers import RecipeSerializer, SubscribeAuthorSerializer


class SubscribeFavoriteShoppingCartMixin:

    @staticmethod
    def create_method(input_model, action_model, author_or_recipe_pk, request):
        user = request.user
        if input_model == Recipe:
            recipe = get_object_or_404(input_model, pk=author_or_recipe_pk)
            serializer = RecipeSerializer(
                instance=recipe, context={'request': request}
            )
            if not action_model.objects.filter(
                recipe=recipe, user=user
            ).exists():
                action_model.objects.create(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if input_model == User:
            author = get_object_or_404(input_model, pk=author_or_recipe_pk)
            serializer = SubscribeAuthorSerializer(
                instance=author, context={'request': request}
            )
            action_model.objects.create(user=user, author=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method(input_model, action_model, author_or_recipe_pk, request):
        user = request.user
        author_or_recipe = get_object_or_404(
            input_model,
            pk=author_or_recipe_pk
        )
        if input_model == Recipe:
            action_model.objects.filter(
                user=user,
                recipe=author_or_recipe
            ).delete()
        if input_model == User:
            action_model.objects.filter(
                user=user,
                author=author_or_recipe
            ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
