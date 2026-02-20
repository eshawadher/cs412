# File: forms.py
# Author: Esha Wadher (eshaaw@bu.edu), 02/20/2026
# Description:
# Defines the form used to create a new Post in the mini_insta app.


from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    '''form to create a new post object'''
    image_url = forms.URLField(label='Image URL', required=False)

    class Meta:
        model = Post
        fields = ['caption']
        