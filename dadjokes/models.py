# File: models.py
# Author: Esha Wadher (eshaaw@bu.edu), 4/3/2026
# Description: Models for the dadjokes app, defining Joke and Picture data models.

from django.db import models

# Create your models here.
class Joke(models.Model):
    '''model taht stores a dad joke with a contributor info and timestamp'''

    #the joke text
    text = models.TextField()

    #name of the person who contrib

    name = models.CharField(max_length=100)

    #timestamp of when the joke was creted

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''return a string rep of the joke'''
        return f"{self.name}: {self.text[:50]}"

class Picture(models.Model):
    '''model to store a silly joke image'''

    #image irl 
    image_url = models.URLField()

    #persons naem who contributed the picture
    name = models.CharField(max_length=100)

    #timestamp of when teh picture was created
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''return a string rep of the pic'''
        return f"{self.name}: {self.image_url[:50]}"
    