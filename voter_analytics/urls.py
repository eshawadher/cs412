# File: urls.py
# Author: Esha Wadher (eshaaw@bu.edu), 02/13/2026
# Description:
# Defines the URL routing for voter analytics application.

from django.urls import path
from . import views

urlpatterns = [
    path("", views.VoterListView.as_view(), name="home"),
    path("voters", views.VoterListView.as_view(), name="voters"),
    path("voter/<int:pk>/", views.VoterDetailView.as_view(), name="voter"),
    path("graphs/", views.GraphsView.as_view(), name="graphs"),
]
