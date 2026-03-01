# File: urls.py
# Author: Esha Wadher (eshaaw@bu.edu), 02/13/2026
# Description:
# Defines the URL routing for the mini_insta application.

from django.urls import path
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView, UpdateProfileView,DeletePostView, UpdatePostView


urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name='create_post'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
]