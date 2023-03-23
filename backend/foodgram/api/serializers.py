import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from recipes.models import IngredientsModel, TagsModel

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserModel
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'id')


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, max_length=128)
    email = serializers.CharField(required=True, max_length=254)


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, max_length=128)
    current_password = serializers.CharField(required=True, max_length=128)


class TagsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source='title')
    color = serializers.CharField()
    slug = serializers.CharField()


class IngredientsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source='title')
    measurement_unit = serializers.CharField()


class Base64ImageField(serializers.Field):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return data


class IngredientsField(serializers.ListField):
    def to_internal_value(self, data):

        print(data)
        return data


class TagsField(serializers.ListField):
    def to_representation(self, objects):

        for obj in objects:
            pass
        return {
            'id': obj.id,
            'name': obj.name,
        }

    def to_internal_value(self, data):
        return TagsModel.objects.filter(pk__in=data)


class RecipesSerializer(serializers.Serializer):
    ingredients = IngredientsField()
    tags = TagsField()
    image = Base64ImageField()
    name = serializers.CharField(source='title')
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()
