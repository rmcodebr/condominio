import logging
from typing import Optional
from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

logger = logging.getLogger(__name__)


def set_auth_cookies(response: Response, access_token: str, refresh_token: Optional[str]=None) -> None:  
  access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
  cookie_settings = {
    'path': settings.COOKIE_PATH,
    'secure': settings.COOKIE_SECURE,
    'httponly': settings.COOKIE_HTTPONLY,
    'samesite': settings.COOKIE_SAMESITE,
    'max_age': access_token_lifetime
  }
  response.set_cookie('access', access_token, **cookie_settings)

  if refresh_token:
    refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
    refresh_cookie_settings = cookie_settings.copy()
    refresh_cookie_settings['max_age'] = refresh_token_lifetime
    response.set_cookie('refresh', refresh_token, **refresh_cookie_settings)

  logged_in_cookie_settings = cookie_settings.copy()
  logged_in_cookie_settings['httponly'] = False
  response.set_cookie('logged_in', 'true', **logged_in_cookie_settings)


class CustomTokenObtainPairView(TokenObtainPairView):
  def post(self, request:Request, *args, **kwargs) -> Response:
    token_res = super().post(request, *args, **kwargs)

    if token_res.status_code == status.HTTP_200_OK:
      access_token = token_res.data.get('access')
      refresh_token = token_res.data.get('refresh')

      if access_token and refresh_token:
        set_auth_cookies(token_res, access_token=access_token, refresh_token=refresh_token)
        token_res.data.pop('access', None)
        token_res.data.pop('refresh', None)

        token_res.data['message'] = 'Login Succesfully'
      else:
        token_res.data['message'] = 'Login Failed'
        logger.error('Access or refresh token not foun in login response data')
    return token_res

class CustomTokenRefreshView(TokenRefreshView):
  def post(self, request:Request, *args, **kwargs) -> Response:
    refresh_token = request.COOKIES.get('refresh')

    if refresh_token:
      request.data['refresh'] = refresh_token
    
    refresh_res = super().post(request, *args, **kwargs)

    if refresh_res.status_code == status.HTTP_200_OK:
      access_token = refresh_res.data.get('access')
      refresh_token = refresh_res.data.get('refresh')

      if access_token and refresh_token:
        set_auth_cookies(refresh_res, access_token=access_token, refresh_token=refresh_token)
        refresh_res.data.pop('access', None)
        refresh_res.data.pop('refresh', None)

        refresh_res.data['message'] = 'Access tokens refreshed succesfully'
      else:
        refresh_res.data['message'] = 'Access or refresh tokens not found in refresh response data'
        logger.error('Access or refresh token not foun in response data')
    return refresh_res

class CustomProviderAuthView(ProviderAuthView):
  def post(self, request:Request, *args, **kwargs) -> Response:
    provider_res = super().post(request, *args, **kwargs)

    if provider_res.status_code == status.HTTP_201_CREATED:
      access_token = provider_res.data.get('access')
      refresh_token = provider_res.data.get('refresh')

      if access_token and refresh_token:
        set_auth_cookies(provider_res, access_token=access_token, refresh_token=refresh_token)
        provider_res.data.pop('access', None)
        provider_res.data.pop('refresh', None)

        provider_res.data['message'] = 'You are logged in Succesfully'
      else:
        provider_res.data['message'] = 'Access or refresh token not foun in provider response data'
        logger.error('Access or refresh token not foun in provider response data')
    return provider_res
  

class LogoutAPIView(APIView):
  def post(self, request: Request, *args, **kwargs):
    response = Response(status=status.HTTP_204_NO_CONTENT)
    response.delete_cookie('access')
    response.delete_cookie('refresh')
    response.delete_cookie('logged_in')
    return response


from typing import List
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from common.renderers import GenericJSONRenderer
from .models import Profile
from .serializers import (
    AvatarUploadSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)

from .tasks import save_profile_avatar

User = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
  page_size = 9
  page_size_query_param = "page_size"
  max_page_size = 100

class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = [GenericJSONRenderer]
    pagination_class = StandardResultsSetPagination
    object_label = "profiles"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    filterset_fields = ["occupation", "gender", "country_of_origin"]

    def get_queryset(self) -> List[Profile]:
        return (
            Profile.objects.exclude(user__is_staff=True)
            .exclude(user__is_superuser=True)
            .filter(occupation=Profile.Occupation.TENANT)
        )
    
class ProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "profile"

    def get_queryset(self) -> QuerySet:
        return Profile.objects.select_related("user").all()

    def get_object(self) -> Profile:
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise Http404("Profile not found")
        
class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateProfileSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "profile"

    def get_queryset(self):
        return Profile.objects.none()

    def get_object(self) -> Profile:
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def perform_update(self, serializer: UpdateProfileSerializer) -> Profile:
        user_data = serializer.validated_data.pop("user", {})
        profile = serializer.save()
        User.objects.filter(id=self.request.user.id).update(**user_data)
        return profile


class AvatarUploadView(APIView):
    def patch(self, request, *args, **kwargs):
        return self.upload_avatar(request, *args, **kwargs)

    def upload_avatar(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = AvatarUploadSerializer(profile, data=request.data)

        if serializer.is_valid():
            image = serializer.validated_data["avatar"]

            image_content = image.read()

            save_profile_avatar.delay(str(profile.id), image_content)

            return Response(
                {"message": "Avatar upload started."}, status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NonTenantProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = [GenericJSONRenderer]
    pagination_class = StandardResultsSetPagination
    object_label = "non_tenant_profiles"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    filterset_fields = ["occupation", "gender", "country_of_origin"]

    def get_queryset(self) -> List[Profile]:
        return (
            Profile.objects.exclude(user__is_staff=True)
            .exclude(user__is_superuser=True)
            .exclude(occupation=Profile.Occupation.TENANT)
        )
