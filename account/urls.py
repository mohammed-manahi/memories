from django.urls import path
from django.contrib.auth import views as auth_views
from account import views

urlpatterns = [
    # Define login url for user login function-based view
    # path('login/', views.user_login, name='login'),
    # Define django authentication urls
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
]
