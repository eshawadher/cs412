# File: forms.py
# Author: Esha Wadher (eshaaw@bu.edu), 02/20/2026
# Description:
# Defines the form used to create a new Post in the mini_insta app.


from django import forms
from .models import Post, Profile

class CreatePostForm(forms.ModelForm):
    '''form to create a new post object'''
    #image_url = forms.URLField(label='Image URL', required=False)

    class Meta:
        model = Post
        fields = ['caption']
class UpdateProfileForm(forms.ModelForm):
    '''Fornm to update an exisitng Profile object'''
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']
        


#  username = models.TextField(blank=True)
#     display_name = models.TextField(blank=True)
#     profile_image_url = models.URLField(blank=True)
#     bio_text = models.TextField(blank=True)
#     join_date = models.DateField(auto_now_add=True)