from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow_user'),
]

