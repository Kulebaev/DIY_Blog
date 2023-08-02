from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('blogs/', views.all_blogs, name='blogs'),
    path('bloggers/', views.all_bloggers, name='bloggers'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
]