# File: apps.py
# Author: Esha Wadher (eshaaw@bu.edu), 02/13/2026
# Description:
# Defines the configuration for the mini_insta Django application.

from django.apps import AppConfig


class MiniInstaConfig(AppConfig):
    """
    Application configuration for the mini_insta Django app.
    This module allows Django to recognize and initialize the app.
    """
    name = 'mini_insta'
