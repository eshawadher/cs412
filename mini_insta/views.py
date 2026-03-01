# File: views.py
# Author: Esha Wadher (eshaaw@bu.edu), 02/13/2026
# Description:
# Contains the class-based views for the mini_insta application.
# These views handle incoming HTTP requests, retrieve Profile
# data from the database, and render the appropriate templates.
# Includes a list view to display all profiles and a detail view
# to display information for a single profile.

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Profile,Post, Photo
from .forms import CreatePostForm, UpdateProfileForm
from django.urls import reverse

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
class CreatePostView(CreateView):
    '''hadnle creation of a new post for a given prof'''
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        '''add prof object to the template context'''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context
    def get_success_url(self):
        '''Redirect to the newly created post's detail page.'''
        return reverse('show_post', kwargs={'pk': self.object.pk})
    def form_valid(self, form):
        '''Attach the Profile FK to the Post, then create a Photo.'''
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile
        saved_form = super().form_valid(form)
        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)
        return saved_form
        # image_url = form.cleaned_data.get('image_url')
        # if image_url:
        #     Photo.objects.create(post=self.object, image_url=image_url)
        # return saved_form
class UpdateProfileView(UpdateView):
    '''handle updating an exisiting profike'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'