# Create your views here.
# File: views.py
# Author: Esha Wadher (eshaaw@bu.edu), 4/3/2026
# Description: Views for the dadjokes app, including regular views and REST API views.

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
import random


from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer

def random_joke(request):
    '''show one random joke and one random pic'''
    jokes = Joke.objects.all()
    pictures = Picture.objects.all()
    joke = random.choice(list(jokes)) if jokes else None
    picture = random.choice(list(pictures)) if pictures else None
    return render(request, 'dadjokes/random.html', {'joke': joke, 'picture': picture})

def jokes_list(request):
    '''show all jokes'''
    jokes = Joke.objects.all()
    return render(request, 'dadjokes/jokes_list.html', {'jokes': jokes})

def joke_detail(request, pk):
    '''show one joke by pk '''
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, 'dadjokes/joke_detail.html', {'joke': joke})

def pictures_list(request):
    '''show all pics'''
    pictures = Picture.objects.all()
    return render(request, 'dadjokes/pictures_list.html', {'pictures': pictures})

def picture_detail(request, pk):
    '''show one picture by pk'''
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'dadjokes/picture_detail.html', {'picture': picture})
#api views

class JokeListAPIView(generics.ListCreateAPIView):
    '''api view to return a listing of all jokes and create a new one'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveAPIView):
    ''''apu view to return a single joke by pk'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer
class PictureListAPIView(generics.ListAPIView):
    '''api view to return a single pic by a pk'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
class PictureDetailAPIView(generics.RetrieveAPIView):
    '''aPI view to return a single picture by primary key.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
class RandomJokeAPIView(APIView):
    '''API view to return one random Joke'''
    def get(self, request):
        jokes = list(Joke.objects.all())
        joke = random.choice(jokes) if jokes else None
        serializer = JokeSerializer(joke)
        return Response(serializer.data)
class RandomPictureAPIView(APIView):
    '''apu view to return one random picture'''
    def get(self, request):
        pictures = list(Picture.objects.all())
        picture = random.choice(pictures) if pictures else None
        serializer = PictureSerializer(picture)
        return Response(serializer.data)
    
