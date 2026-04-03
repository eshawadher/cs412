# File: admin.py
# Author: Esha Wadher (eshaaw@bu.edu), 4/3/2026
# Description: Admin registration for the dadjokes app models.

from django.contrib import admin
from .models import Joke, Picture

# Register your models here.
admin.site.register(Joke)
admin.site.register(Picture)