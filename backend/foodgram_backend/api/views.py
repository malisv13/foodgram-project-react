from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet

from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from recipes.models import (Favorite, Ingredient, IngredientsInRecipe, Recipe,
                            ShoppingCart, Tag)
from services.build_shopping_cart_file import BuildShoppingCartFileService
from users.models import Subscribe, User
from .filters import RecipeFilter
from .mixins import SubscribeFavoriteShoppingCartMixin
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeWriteSerializer,
                          RecipeGetSerializer, SubscriptionSerializer,
                          TagSerializer)


class CustomUserViewSet(UserViewSet, SubscribeFavoriteShoppingCartMixin):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    pagination_class = CustomPagination

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,),
            pagination_class=CustomPagination)
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        if request.method == 'POST':
            return self.create_method(User, Subscribe, id, request)
        elif request.method == 'DELETE':
            return self.delete_method(User, Subscribe, id, request)


class RecipeViewSet(viewsets.ModelViewSet, SubscribeFavoriteShoppingCartMixin):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'create', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipeWriteSerializer

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.create_method(Recipe, Favorite, pk, request)
        elif request.method == 'DELETE':
            return self.delete_method(Recipe, Favorite, pk, request)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            pagination_class=None)
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.create_method(Recipe, ShoppingCart, pk, request)
        elif request.method == 'DELETE':
            return self.delete_method(Recipe, ShoppingCart, pk, request)

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request, **kwargs):
        recipes_ids = ShoppingCart.objects.filter(
            user=request.user).values_list('recipe_id')
        ingredients = IngredientsInRecipe.objects.filter(
            recipe__in=recipes_ids).values('ingredient__name',
                                           'ingredient__measurement_unit'
                                           ).annotate(amount=Sum('amount'))

        service = BuildShoppingCartFileService(ingredients)
        response = HttpResponse(service.final_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format(service.filename)
        )
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', )
    pagination_class = None
