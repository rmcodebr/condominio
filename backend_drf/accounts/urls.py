from django.urls import path, re_path
from .views import (CustomProviderAuthView, CustomTokenObtainPairView, CustomTokenRefreshView, LogoutAPIView)
from .views import (
    AvatarUploadView,
    ProfileListAPIView,
    ProfileDetailAPIView,
    ProfileUpdateAPIView,
    NonTenantProfileListAPIView,
)
urlpatterns = [
    re_path(
        r"^o/(?P<provider>\S+)/$",
        CustomProviderAuthView.as_view(),
        name="provider-auth",
    ),
    path("login/", CustomTokenObtainPairView.as_view()),
    path("refresh/", CustomTokenRefreshView.as_view()),
    path("logout/", LogoutAPIView.as_view()),

    path("all/", ProfileListAPIView.as_view(), name="profile-list"),
    path(
        "non-tenant-profiles/",
        NonTenantProfileListAPIView.as_view(),
        name="non-tenant-profiles",
    ),
    path("user/my-profile/", ProfileDetailAPIView.as_view(), name="profile-detail"),
    path("user/update/", ProfileUpdateAPIView.as_view(), name="profile-update"),
    path("user/avatar/", AvatarUploadView.as_view(), name="avatar-upload"),
]


# from django.urls import path

# urlpatterns = [
#     path(
#         "o/<str:provider>/",
#         CustomProviderAuthView.as_view(),
#         name="provider-auth",
#     ),
#     path("login/", CustomTokenObtainPairView.as_view()),
#     path("refresh/", CustomTokenRefreshView.as_view()),
#     path("logout/", LogoutAPIView.as_view()),
# ]
