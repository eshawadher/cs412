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
    
class Photo(models.Model):
    '''encap the dat of a phot associuate with a post'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''return a string rep of thsi photo'''
        return f'Photo for post {self.post.pk} at {self.timestamp}'



