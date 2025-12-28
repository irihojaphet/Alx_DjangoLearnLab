from django.urls import path
from .views import feed, LikePostView, UnlikePostView

# No router here - viewsets are registered in main urls.py
# This file only contains non-viewset endpoints
urlpatterns = [
    path('feed/', feed, name='feed'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like_post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike_post'),
]