from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, UserLoginViewSet, UserLogoutViewSet, SetPasswordViewSet, TagsViewSet, IngredientsViewSet, RecipesViewSet
app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1_auth = routers.DefaultRouter()

router_v1.register('users/set_password', SetPasswordViewSet, basename='set_password')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('recipes', RecipesViewSet, basename='recipes')
router_v1_auth.register('token/login', UserLoginViewSet, basename='login')
router_v1_auth.register('token/logout', UserLogoutViewSet, basename='logout')

urlpatterns = [
    path('auth/', include(router_v1_auth.urls)),
    path('', include(router_v1.urls)),
]