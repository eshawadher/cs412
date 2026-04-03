# File: urls.py
# Author: Esha Wadher (eshaaw@bu.edu), 4/3/2026
# Description: URL patterns for the dadjokes app.

from django.urls import path
from . import views

urlpatterns = [
    # Regular views
    path('', views.random_joke, name='random_joke'),
    path('random', views.random_joke, name='random_joke2'),
    path('jokes', views.jokes_list, name='jokes_list'),
    path('joke/<int:pk>', views.joke_detail, name='joke_detail'),
    path('pictures', views.pictures_list, name='pictures_list'),
    path('picture/<int:pk>', views.picture_detail, name='picture_detail'),

    # API endpoints
    path('api/', views.RandomJokeAPIView.as_view(), name='api_random_joke'),
    path('api/random', views.RandomJokeAPIView.as_view(), name='api_random_joke2'),
    path('api/jokes', views.JokeListAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', views.JokeDetailAPIView.as_view(), name='api_joke_detail'),
    path('api/pictures', views.PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', views.PictureDetailAPIView.as_view(), name='api_picture_detail'),
    path('api/random_picture', views.RandomPictureAPIView.as_view(), name='api_random_picture'),
]