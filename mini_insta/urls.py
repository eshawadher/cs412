# File: urls.py
# Author: Esha Wadher (eshaaw@bu.edu), 02/13/2026
# Description:
# Defines the URL routing for the mini_insta application.

from django.urls import path
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
]