# File: views.py
# Author: Esha Wadher (eshaaw@bu.edu), 02/13/2026
# Description:
# Contains the class-based views for the mini_insta application.
# These views handle incoming HTTP requests, retrieve Profile
# data from the database, and render the appropriate templates.
# Includes a list view to display all profiles and a detail view
# to display information for a single profile.

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile,Post

# Create your views here.
class ProfileListView(ListView):
    '''Define a class to show all the profiles'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''Show details for one profile'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class PostDetailView(DetailView):
    '''show details for one post, incluidng all its pics'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'
