from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('account/', include('django.contrib.auth.urls')),
    path('search/', search_results, name='search'),
    # path(r'^api/merch/$', ProdsList.as_view()),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', AuthUserRegistrationView.as_view(), name='register'),
    path('login', AuthUserLoginView.as_view(), name='login'),
    path('users', UserListView.as_view(), name='users'),
    path('product/<post>', project_view, name='product'),
    path("logout", logout_request, name="logout"),

]