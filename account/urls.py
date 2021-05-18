from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from . import views


app_name = 'account'

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='account/login.html',form_class=LoginForm, 
    redirect_authenticated_user=True,), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='account:login'), name='logout'),
    path('register/', views.register_user, name='register'),
    path('user/profile/',views.update_user,name='update_user'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/@<username>/', views.user_detail, name='user_detail'),
]
