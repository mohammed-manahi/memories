from django.urls import path, include
from django.contrib.auth import views as auth_views
from account import views

urlpatterns = [
    # Define login url for user login function-based view
    # path('login/', views.user_login, name='login'),
    # Define django authentication urls
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password-change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # The below url pattern can be used instead of the above url patterns
    path('', include('django.contrib.auth.urls')),
    # Define user dashboard url
    path('', views.dashboard, name='dashboard'),
    # Define user registration url
    path('register/', views.register, name='register'),

]
