# File: views.py
# Author: Esha Wadher (eshaaw@bu.edu), 02/13/2026
# Description:
# Contains the class-based views for the mini_insta application.
# These views handle incoming HTTP requests, retrieve Profile
# data from the database, and render the appropriate templates.
# Includes a list view to display all profiles and a detail view
# to display information for a single profile.

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,View
from .models import Profile,Post, Photo, Follow, Like
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import ProfileSerializer, PostSerializer



# Create your views here.

class ProfileAuthMixin(LoginRequiredMixin):
    '''used to requre a login '''
    
    def get_login_url(self):
        '''return the login URL'''
        return reverse('login')
    
    def get_profile(self):
        '''return the Profile associated with the logged-in user'''
        return self.request.user.profile
    
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

class ShowMyProfileView(ProfileAuthMixin, DetailView):
    '''show the prof of the logges in user'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        '''Return the Profile for the logged-in user'''
        return self.get_profile()


class PostDetailView(DetailView):
    '''show details for one post, incluidng all its pics'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'
class CreatePostView(ProfileAuthMixin, CreateView):
    '''hadnle creation of a new post for a given prof'''
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        '''add prof object to the template context'''
        context = super().get_context_data(**kwargs)
        # pk = self.kwargs['pk']
        # profile = Profile.objects.get(pk=pk)
        profile = self.get_profile()
        context['profile'] = profile
        return context
    def get_success_url(self):
        '''Redirect to the newly created post's detail page.'''
        return reverse('show_post', kwargs={'pk': self.object.pk})
    def form_valid(self, form):
        '''Attach the Profile FK to the Post, then create a Photo.'''
        # pk = self.kwargs['pk']
        profile = self.get_profile()
        form.instance.profile = profile
        saved_form = super().form_valid(form)
        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)
        return saved_form
    
class UpdateProfileView(ProfileAuthMixin, UpdateView):
    '''handle updating an exisiting profike'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        '''returnt thr prof for the logged in user '''
        return self.get_profile()
class DeletePostView (ProfileAuthMixin, DeleteView):
    '''handle post deletiobn'''
    model = Post
    template_name ='mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        '''add post and profile to connect'''
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        context['profile'] = self.get_object().profile
        return context
    
    def get_success_url(self):
        '''redirect to main prof page'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
class UpdatePostView(ProfileAuthMixin,UpdateView):
    '''handle updating a post'''
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_success_url(self):
        '''Redirect to the post page after update.'''
        return reverse('show_post', kwargs={'pk': self.object.pk})

class ShowFollowersDetailView(DetailView):
    '''show all followers of a Profile.'''
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    '''show all profiles that a Profile is following.'''
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'
class PostFeedListView(ProfileAuthMixin, ListView):
    '''show the post feed for a single Profile.'''
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        '''return posts from profiles that this profile follows.'''
        profile = self.get_profile()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''add profile to context.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context
    

class SearchView(ProfileAuthMixin, ListView):
    '''handle seach for profiles and posts'''
    model = Post
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''handle the request, showing search form if no query'''
        if 'query' not in request.GET:
            profile = self.get_profile()
            return render(request, 'mini_insta/search.html')
        return super ().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        '''return posts matching the q set'''
        query = self.request.GET.get('query','')
        return Post.objects.filter(caption__icontains=query)
    def get_context_data(self, **kwargs):
        '''add prof, query, posts, and matching profiles to context'''
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')
        profile = self.get_profile()
        context['profile'] = profile
        context['query'] = query
        context['posts'] = self.get_queryset()
        context['profiles'] = Profile.objects.filter(username__icontains=query) | Profile.objects.filter(display_name__icontains=query) | Profile.objects.filter(bio_text__icontains=query)
        return context
class CreateProfileView(CreateView):
    '''create new prof and user'''
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context
    def form_valid(self,form):
        '''proccesses the user and profile form'''
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context['user_form'] = user_form 

            return self.render_to_response(context)
    def get_success_url(self):
        '''redirect to the new profile after creation'''
        return reverse('show_my_profile')
class FollowProfileView(ProfileAuthMixin, View):
    '''create a follwo relationship between loggied in user and another profile'''
    def dispatch(self, request, *args, **kwargs):
        '''handle follow action'''
        pk = self.kwargs['pk']
        profile_to_follow = Profile.objects.get(pk=pk)

        my_profile = self.get_profile()
        if my_profile != profile_to_follow:
            if not Follow.objects.filter(profile=profile_to_follow, follower_profile = my_profile).exists():
                Follow.objects.create(profile=profile_to_follow, follower_profile = my_profile)
        
        return redirect('show_profile', pk=pk)
class UnfollowProfileView(ProfileAuthMixin, View):
    '''delte a follower relationship'''
    def dispatch(self, request, *args, **kwargs):
        '''handle unfollow action'''
        pk = self.kwargs['pk']
        profile_to_unfollow = Profile.objects.get(pk=pk)

        my_profile = self.get_profile()
        Follow.objects.filter(profile=profile_to_unfollow, follower_profile = my_profile).delete()
        
        return redirect('show_profile', pk=pk)
class LikePostView(ProfileAuthMixin, View):
    '''create a like on a post'''
    def dispatch(self, request, *args, **kwargs):
        '''handle likig post action'''
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)

        my_profile = self.get_profile()
        if my_profile != post.profile:
            if not Like.objects.filter(post=post, profile = my_profile).exists():
                Like.objects.create(post=post, profile = my_profile)
        
        return redirect('show_post', pk=pk)
    
class UnlikePostView(ProfileAuthMixin, View):
    '''delete  a like on a post'''
    def dispatch(self, request, *args, **kwargs):
        '''handle unlikig post action'''
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        my_profile = self.get_profile()
        Like.objects.filter(post=post, profile = my_profile).delete()
        return redirect('show_post', pk=pk)
    
# API view to handle login 
class LoginAPIView(APIView):
    '''API View to handle login by credentials, return an AuthToken.'''
    # open up this view to allow unauthenticated users
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        '''authenticate user and return token and profile data.'''
        user = authenticate(
            request,
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        print(f"LoginAPIView.post(): user={user}")
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            profile = Profile.objects.get(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'profile_id': profile.id,
            })
        return Response({'error': 'Invalid credentials'}, status=400)

# API view to list all profiles
class ProfileListAPIView(generics.ListAPIView):
    '''an API view to return a listing of Profiles.'''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# API view to retrieve one profile
class ProfileDetailAPIView(generics.RetrieveAPIView):
    '''an API view to return a single Profile.'''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# API view to list posts for one profile
class ProfilePostsAPIView(generics.ListAPIView):
    '''an API view to return all posts for a given profile.'''
    serializer_class = PostSerializer

    def get_queryset(self):
        '''return posts for the profile specified by pk.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return profile.get_all_posts()

# API view to return the feed for one profile
class ProfileFeedAPIView(generics.ListAPIView):
    '''an API view to return the feed for a given profile.'''
    serializer_class = PostSerializer

    def get_queryset(self):
        '''return feed posts for the profile specified by pk.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return profile.get_post_feed()

# API view to create a new post
class CreatePostAPIView(generics.CreateAPIView):
    '''an API view to create a new Post.'''
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        '''set the profile when creating a post.'''
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(profile=profile)