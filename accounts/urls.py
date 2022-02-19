from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name='password_reset_complete'),
    path('account/',
         views.accountSettings,
         name="account"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user-page"),
    path('', views.home, name='home'),
    path('loadings/', views.loadings, name='loadings'),
    path('company/<str:pk_test>/', views.company, name='company'),
    path('create_loading/<int:pk>', views.create_loading, name="create_loading"),
    path('update_loading/<str:pk>/', views.update_loading, name="update_loading"),
    path('delete_loading/<str:pk>/', views.delete_loading, name="delete_loading"),

]
