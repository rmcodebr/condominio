from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField

from rest_framework import serializers


User = get_user_model()

class CreateUserSerializer(UserCreateSerializer):
  class Meta(UserCreateSerializer.Meta):
    model = User
    fields = ['id', 'username', 'first_name', 'last_name', 'password']

class CustomUserSerializer(UserSerializer):
  full_name = serializers.ReadOnlyField(source="get_full_name")
  gender = serializers.ReadOnlyField(source="profile.gender")
  slug = serializers.ReadOnlyField(source="profile.slug")
  phone_number = serializers.CharField(source="profile.phone_number", read_only=True)
  occupation = serializers.ReadOnlyField(source="profile.occupation")
  country = serializers.CharField(source="profile.country_of_origin", read_only=True)
  city = serializers.ReadOnlyField(source="profile.city_of_origin")
  avatar = serializers.ReadOnlyField(source="profile.avatar.url")
  reputation = serializers.ReadOnlyField(source="profile.reputation")

  class Meta(UserSerializer.Meta):
    model = User
    fields = ['id', 'email', 'first_name', 'last_name', 'username', 'slug',
              'full_name', 'gender','occupation', 'phone_number','country',
              'city', 'reputation', 'date_joined', 'avatar',
              ]
    read_only_fields = ['id', 'email', 'date_joined']
