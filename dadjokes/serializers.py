# File: serializers.py
# Author: Esha Wadher (eshaaw@bu.edu), 4/3/2026
# Description: Serializers for the dadjokes app, converting Joke and 
# Picture model instances to JSON format for the REST API.
from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    '''serializer to covert joke object o and from json'''
    class Meta:
        model = Joke
        fields = ['id', 'text', 'name', 'timestamp']
class PictureSerializer(serializers.ModelSerializer):
    '''serializer to onver picture objects to form json'''
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'name', 'timestamp']
