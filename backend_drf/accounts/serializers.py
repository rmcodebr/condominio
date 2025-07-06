from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField

from rest_framework import serializers

from .models import Profile


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


class ProfileSerializer(serializers.ModelSerializer):
  first_name = serializers.ReadOnlyField(source="user.first_name")
  last_name = serializers.ReadOnlyField(source="user.last_name")
  username = serializers.ReadOnlyField(source="user.username")
  full_name = serializers.ReadOnlyField(source="user.get_full_name")
  country_of_origin = CountryField(name_only=True)
  avatar = serializers.SerializerMethodField()
  date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
  # apartment = serializers.SerializerMethodField()
  # average_rating = serializers.SerializerMethodField()

  class Meta:
    model = Profile
    fields = [
      "id",
      "slug",
      "first_name",
      "last_name",
      "username",
      "full_name",
      "gender",
      "country_of_origin",
      "city_of_origin",
      "bio",
      "occupation",
      "reputation",
      "date_joined",
      "avatar",
      # "apartment",
      # "average_rating",
    ]
  
  def get_avatar(self, obj: Profile) -> str | None:
    try:
      return obj.avatar.url
    except AttributeError:
      return None
    


    

class UpdateProfileSerializer(serializers.ModelSerializer):
  first_name = serializers.CharField(source="user.first_name")
  last_name = serializers.CharField(source="user.last_name")
  username = serializers.CharField(source="user.username")
  country_of_origin = CountryField(name_only=True)

  class Meta:
    model = Profile
    fields = [
      "first_name",
      "last_name",
      "username",
      "gender",
      "country_of_origin",
      "city_of_origin",
      "bio",
      "occupation",
      "phone_number",
    ]

class AvatarUploadSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ["avatar"]