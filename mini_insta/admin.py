# File: admin.py
# Author: Esha Wadher (eshaaw@bu.edu), 02/13/2026
# Description:
# Registers the Profile model with the Django admin interface so
# that profiles can be viewed, added, edited, and deleted through
# the built-in administrative dashboard.

from django.contrib import admin
from .models import Profile, Post, Photo, Follow, Comment, Like
# Register your models here.
"""
Registers the Profile model so it can be managed through
the Django administrative interface.
"""
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)