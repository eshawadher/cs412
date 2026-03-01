# File: models.py
# Author: Esha Wadher (eshaaw@bu.edu), 02/13/2026
# Description:
# The Profile model represents a user's profile and stores
# information such as username, display name, profile image URL,
# biography text, and the date the profile was created.

from django.db import models
from django.urls import reverse

# # Create your models here.
class Profile(models.Model):
    '''encap the data of a users profile'''
    #define data attributes of teh Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.display_name} by {self.username}'
    def get_all_posts(self):
        '''return a qset of all posts creted by this prof ordered by timessta,p'''
        return Post.objects.filter(profile=self).order_by('timestamp')
    def get_absolute_url(self):
        '''retyrn url to display this prof'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_followers(self):
        '''get followers that follow this profile'''
        return [f.follower_profile for f in Follow.objects.filter(profile=self)]
    def get_num_followers(self):
        '''return the number of followers.'''
        return len(self.get_followers())
    def get_following(self):
        '''return a list of Profiles that this person follows.'''
        return [f.profile for f in Follow.objects.filter(follower_profile=self)]
    def get_num_following(self):
        '''Return the number of profiles being followed.'''
        return len(self.get_following())
    def get_post_feed(self):
        '''return a list of Posts from profiles that this profile follow'''
        following = self.get_following()
        return Post.objects.filter(profile__in=following).order_by('-timestamp')
class Post(models.Model):
    '''encap data of an insta post'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''return string interp of post'''
        return f'Post by {self.profile.username} at {self.timestamp}'
    def get_absolute_url(self):
        '''return the URL to disaply this Post'''
        return Photo.objects.filter(post=self)
    
    def get_all_photos(self):
        '''return qset of all photos in post'''
        return Photo.objects.filter(post=self)
    def get_all_comments(self):
        '''Return all comments on this Post.'''
        return Comment.objects.filter(post=self)
    def get_likes(self):
        '''Return all likes on this Post.'''
        return Like.objects.filter(post=self)
    
class Photo(models.Model):
    '''encap the dat of a phot associuate with a post'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''return a string rep of thsi photo'''
        if self.image_file:
            return f'Photo (image_file) for post {self.post.pk} at {self.timestamp}'
        return f'Photo (image_url) for post {self.post.pk} at {self.timestamp}'
    def get_image_url(self):
        '''return the URL to the image, whether file or URL'''
        if self.image_file:
            return self.image_file.url
        return self.image_url
class Follow(models.Model):
    '''one Profile following another.'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_profile')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this follow.'''
        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'

class Comment(models.Model):
    '''Encapsulates the idea of a profile commenting'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this object.'''
        return f'Comment by {self.profile.display_name} on post {self.post.pk}'
class Like(models.Model):
    '''Encapsulates the idea of a Profile likes'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this Like object.'''
        return f'Like by {self.profile.display_name} on post {self.post.pk}'
