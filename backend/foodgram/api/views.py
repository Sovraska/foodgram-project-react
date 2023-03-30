from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, IngredientsModel, RecipeIngredient,
                            RecipesModel, Shopping, TagsModel)
from users.models import Follow

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthenticatedOrReadOnlyPermission
from .serializers import (ChangePasswordSerializer, FollowSerializer,
                          IngredientsSerializer, RecipeFollowSerializer,
                          RecipeGetSerializer, RecipesSerializer,
                          TagSerializer, UserLoginSerializer, UserSerializer)

UserModel = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()

    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    permission_classes = (AllowAny,)

    lookup_field = 'id'

    class Meta:
        model = UserModel

    def perform_create(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    @action(
        detail=False,
        methods=['post'],
        url_path='set_password',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():

            user = self.request.user
            if not check_password(
                    serializer.validated_data['current_password'],
                    user.password
            ):
                message = "Current Password is incorrect"
                return Response(message, status=status.HTTP_401_UNAUTHORIZED)

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me_data(self, request):
        """Возможность получения Пользователя данных о себе

        GET запрос"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(UserModel, pk=kwargs.get('id'))
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=(FollowSerializer,)
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(UserModel, id=id)
        if self.request.method == 'POST':
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данного пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if user == author:
                return Response(
                    {'errors': 'Нельзя подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                follow, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if Follow.objects.filter(user=user, author=author).exists():
            follow = get_object_or_404(Follow, user=user, author=author)
            follow.delete()
            return Response(
                'Подписка успешно удалена',
                status=status.HTTP_204_NO_CONTENT
            )
        if user == author:
            return Response(
                {'errors': 'Нельзя отписаться от самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'errors': 'Вы не подписаны на данного пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLoginViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin,
):
    """Вьюсет логина"""
    permission_classes = (AllowAny,)

    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, )

        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get('password')
        email = serializer.validated_data.get('email')

        if not UserModel.objects.filter(email=email).exists():
            message = "email is incorrect"
            return Response(
                data=message,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(UserModel, email=email)
        if not check_password(password, user.password):
            message = "password is incorrect"
            return Response(
                data=message,
                status=status.HTTP_400_BAD_REQUEST
            )

        token, created = Token.objects.get_or_create(user=user)

        response = {
            "auth_token": str(token)
        }

        return Response(
            data=response,
            status=status.HTTP_201_CREATED
        )


class UserLogoutViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin,
):
    permission_classes = (IsAuthenticated,)

    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        Token.objects.filter(user_id=self.request.user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagsViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None

    queryset = TagsModel.objects.all()


class IngredientsViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    permission_classes = (AllowAny,)
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None

    queryset = IngredientsModel.objects.all()


class RecipesViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnlyPermission,)

    queryset = RecipesModel.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('Рецепт успешно удален',
                        status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipesSerializer

    def get_queryset(self):
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited is not None and int(is_favorited) == 1:
            return RecipesModel.objects.filter(
                favorites__user=self.request.user
            )
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_in_shopping_cart is not None and int(is_in_shopping_cart) == 1:
            return RecipesModel.objects.filter(
                recipe_cart__user=self.request.user
            )
        return RecipesModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST', 'DELETE'], )
    def favorite(self, request, pk):
        if self.request.method == 'POST':
            return post_obj(request, pk, Favorite, RecipeFollowSerializer)
        return delete_obj(request, pk, Favorite)

    @action(detail=True, methods=['POST', 'DELETE'], )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return post_obj(request, pk, Shopping, RecipeFollowSerializer)
        return delete_obj(request, pk, Shopping)

    @action(detail=False, methods=['GET'], )
    def download_shopping_cart(self, request):
        if not request.user.cart.exists():
            return Response(
                'В корзине нет товаров', status=status.HTTP_400_BAD_REQUEST)

        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__recipe_cart__user=request.user)
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list(
                'ingredient__name',
                'total_amount',
                'ingredient__measurement_unit'
            )
        )

        text = ''
        for ingredient in ingredients:
            text += '{} - {} {}. \n'.format(*ingredient)

        file = HttpResponse(
            'Покупки:\n' + text, content_type='text/plain'
        )

        file['Content-Disposition'] = ('attachment; filename=cart.txt')
        return file


class FollowListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)


def delete_obj(request, pk, model):
    recipe = get_object_or_404(RecipesModel, pk=pk)
    if model.objects.filter(user=request.user, recipe=recipe).exists():
        follow = get_object_or_404(model, user=request.user,
                                   recipe=recipe)
        follow.delete()
        return Response(
            'Рецепт успешно удален из избранного/списка покупок',
            status=status.HTTP_204_NO_CONTENT
        )
    return Response(
        {'errors': 'Данного рецепта не было в избранном/списке покупок'},
        status=status.HTTP_400_BAD_REQUEST
    )


def post_obj(request, pk, model, serializer):
    recipe = get_object_or_404(RecipesModel, pk=pk)
    if model.objects.filter(user=request.user, recipe=recipe).exists():
        return Response(
            {'errors': 'Рецепт уже есть в избранном/списке покупок'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    model.objects.get_or_create(user=request.user, recipe=recipe)
    data = serializer(recipe).data
    return Response(data, status=status.HTTP_201_CREATED)
