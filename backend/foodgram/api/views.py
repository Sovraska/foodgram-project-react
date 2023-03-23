from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer, UserLoginSerializer, ChangePasswordSerializer, TagsSerializer, IngredientsSerializer, RecipesSerializer
from recipes.models import TagsModel, IngredientsModel, RecipesModel

UserModel = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()

    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    permission_classes = (AllowAny, )

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
            if not check_password(serializer.validated_data['current_password'], user.password):
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
        user = get_object_or_404(UserModel, pk=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLoginViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin,
):
    """Вьюсет логина"""
    permission_classes = (AllowAny,)

    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,)

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


class SetPasswordViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin,
):
    permission_classes = (IsAuthenticated, )

    serializer_class = ChangePasswordSerializer


class TagsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = TagsSerializer
    pagination_class = None
    
    queryset = TagsModel.objects.all()


class IngredientsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = IngredientsSerializer
    pagination_class = None

    queryset = IngredientsModel.objects.all()


class RecipesViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):

    permission_classes = (IsAuthenticated,)
    serializer_class = RecipesSerializer

    queryset = RecipesModel.objects.all()