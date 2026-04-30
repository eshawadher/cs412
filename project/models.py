# File: models.py
# Author: Esha Wadher (eshaaw@bu.edu), 04/19/2026
# Description:
# These models represent a travel planning and bucket list application.
# The application allows users to create profiles, browse destinations
# by country, save destinations to a bucket list, plan trips, and leave
# comments or recommendations on destinations.

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class UserProfile(models.Model):
    """encapsulates the data of a user's travel profile"""

    name = models.TextField()
    age = models.PositiveIntegerField()
    biography = models.TextField(blank=True)
    profile_pic = models.ImageField(blank=True)
    date_joined = models.DateField(auto_now_add=True)
    places_traveled = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """return a string representation of this model instance"""
        return self.name

    def get_absolute_url(self):
        """return the URL to display this profile"""
        return reverse("show_profile", kwargs={"pk": self.pk})

    def get_bucket_list(self):
        """return all bucket list entries for this user"""
        return BucketListEntry.objects.filter(user=self)

    def get_trip_plans(self):
        """return all trip plans for this user"""
        return TripPlan.objects.filter(user=self)

    def get_comments(self):
        """return all comments written by this user"""
        return Comment.objects.filter(user=self)


class Country(models.Model):
    """encapsulates data for a country"""

    name = models.TextField()
    continent = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    country_code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        """return a string representation of this country"""
        return self.name

    def get_absolute_url(self):
        """return the URL to display this country"""
        return reverse("show_country", kwargs={"pk": self.pk})

    def get_destinations(self):
        """return all destinations in this country"""
        return Destination.objects.filter(country=self)


class Destination(models.Model):
    """encapsulates data for a travel destination"""

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        """return a string representation of this destination"""
        return f"{self.name}, {self.country.name}"

    def get_absolute_url(self):
        """return the URL to display this destination"""
        return reverse("show_destination", kwargs={"pk": self.pk})

    def get_bucket_list_entries(self):
        """return all bucket list entries for this destination"""
        return BucketListEntry.objects.filter(destination=self)

    def get_comments(self):
        """return all comments on this destination"""
        return Comment.objects.filter(destination=self)


class BucketListEntry(models.Model):
    """encapsulates a destination saved to a user's bucket list"""

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    STATUS_CHOICES = [
        ("must_visit", "Must Visit"),
        ("upcoming", "Upcoming"),
        ("visited", "Visited"),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="must_visit"
    )
    notes = models.TextField(blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "destination")

    def __str__(self):
        """return a string representation of this bucket list entry"""
        return f"{self.user.name} - {self.destination.name}"

    def get_absolute_url(self):
        """return the URL to display this bucket list entry"""
        return reverse("show_bucket", kwargs={"pk": self.pk})


class TripPlan(models.Model):
    """encapsulates a user's planned or completed trip"""

    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("booked", "Booked"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    entry = models.ForeignKey(BucketListEntry, on_delete=models.CASCADE)
    travel_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planning")
    notes = models.TextField(blank=True)

    def __str__(self):
        """return a string representation of this trip plan"""
        return f"{self.user.name} - {self.entry.destination.name} ({self.travel_date})"

    def get_absolute_url(self):
        """return the URL to display this trip plan"""
        return reverse("show_trip", kwargs={"pk": self.pk})


class Comment(models.Model):
    """encapsulates a user comment or recommendation on a destination"""

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    def __str__(self):
        """return a string representation of this comment"""
        return f"Comment by {self.user.name} on {self.destination.name}"


class ItineraryItem(models.Model):
    '''represents a single activity or event within a trip plan's itinerary.'''
    trip = models.ForeignKey(
        TripPlan, on_delete=models.CASCADE, related_name="itinerary_items"
    )
    day = models.IntegerField()
    time = models.TimeField(blank=True, null=True)
    activity = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        '''returns the day number and activity name as the string representation.'''
        return f"Day {self.day}: {self.activity}"


class DestinationRating(models.Model):
    '''represents a user's numerical rating (1–10) and optional written review for a destination. Ratings are validated to fall within the 1–10 range.'''
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    review = models.TextField(blank=True)

    def __str__(self):
        '''returns the destination name and rating as the string representation.'''
        return f"{self.destination.name} - {self.rating} / 10"
