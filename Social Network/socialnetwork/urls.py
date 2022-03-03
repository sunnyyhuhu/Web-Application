
from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.global_action, name='home'),
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('global', views.global_action, name='global'),
    path('profile', views.profile_action, name='profile'),
    path('other/<int:user_id>', views.other_action, name='other'),
    path('follower', views.follower_action, name='follower'),
    path('logout', views.logout_action, name='logout'),
    path('photo/<int:user_id>', views.photo_action, name='photo'),
    path('follow/<int:user_id>', views.follow_action, name='follow'),
    path('unfollow/<int:user_id>', views.unfollow_action, name='unfollow'),
]