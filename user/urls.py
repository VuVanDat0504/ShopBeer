from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import test,UserDetail,ChangePassword,MyUsers,UserProfile,CustomTokenObtainPairView

urlpatterns = [
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/<int:pk>/',UserDetail.as_view(),name='user-detail'),
    path('password_change/',ChangePassword.as_view(),name='change-password'),
    # login and get
    path('myUser/', MyUsers.as_view(), name='user'),
    path('profile/', UserProfile.as_view(), name='user'),

    # path('user/<int:pk>/',UserDetail.as_view(),name='user-detail'),

    path('test/', test.as_view(), name='test'),
]