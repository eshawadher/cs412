from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import DestinationListView, DestinationDetailView, UserProfileListView, UserProfileDetailView, BucketListEntryListView, BucketListEntryCreateView, BucketListEntryUpdateView, BucketListEntryDeleteView
from .views import TripPlanListView, TripPlanCreateView, TripPlanUpdateView, TripPlanDeleteView, CommentCreateView, CountryDetailView, ItineraryCreateView, DestinationRatingCreateView, ItineraryItemDelete
from .views import *
#urls for the app
urlpatterns = [
    path('', DestinationListView.as_view(), name='home'),
    path('destinations/', DestinationListView.as_view(), name='destinations'),
    path('destination/<int:pk>/', DestinationDetailView.as_view(), name='show_destination'),

    path('profiles/', UserProfileListView.as_view(), name='profiles'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='show_profile'),

    path('bucket/', BucketListEntryListView.as_view(), name='bucket_list'),
    path('bucket/create/<int:destination_pk>/', BucketListEntryCreateView.as_view(), name='create_bucket'),
    path('bucket/<int:pk>/update/', BucketListEntryUpdateView.as_view(), name='update_bucket'),
    path('bucket/<int:pk>/delete/', BucketListEntryDeleteView.as_view(), name='delete_bucket'),

    path('trips/', TripPlanListView.as_view(), name='trips'),
    path('trip/create/<int:entry_pk>/', TripPlanCreateView.as_view(), name='create_trip'),
    path('trip/<int:pk>/update/', TripPlanUpdateView.as_view(), name='update_trip'),
    path('trip/<int:pk>/delete/', TripPlanDeleteView.as_view(), name='delete_trip'),


    path('destination/<int:destination_pk>/comment/create/', CommentCreateView.as_view(), name='create_comment'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('login/', LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='destinations'), name='logout'),
    path('country/<int:pk>/', CountryDetailView.as_view(), name='show_country'),
    path('trip/<int:trip_pk>/itinerary/create/', ItineraryCreateView.as_view(), name='create_itinerary'),
    path('destination/<int:destination_pk>/rating/create/', DestinationRatingCreateView.as_view(), name='create_rating'),
    path('destinations/', DestinationListView.as_view(), name='destinations'),
    path('destination/create/', DestinationCreateView.as_view(), name='create_destination'),
    path('country/create/', CountryCreateView.as_view(), name='create_country'),
    path('itinerary/<int:pk>/delete/', ItineraryItemDelete.as_view(), name='delete_itinerary'),
    path('profile/me/', MyProfileView.as_view(), name='my_profile'),
    path('country/<int:pk>/', CountryDetailView.as_view(), name='country_detail'),
    path('country/<int:pk>/', CountryDetailView.as_view(), name='show_country'),
] 