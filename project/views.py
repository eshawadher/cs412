# File: views.py
# Author: Esha Wadher (eshaaw@bu.edu), April 29, 2026
# Description: Defines the views for the Travel Bucket List project,
# including destination browsing, bucket list management, trip planning,
# comments, ratings, and user profile pages.

import json

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.utils import timezone
from django.contrib import messages
from django.views import View


from .models import (
    UserProfile,
    Country,
    Destination,
    BucketListEntry,
    TripPlan,
    Comment,
    ItineraryItem,
    DestinationRating,
)

 
class ProjectAuthMixin(LoginRequiredMixin):
    '''mixin that enforces login requirements across all project views and provides a helper method to retrieve the current user's profile. '''
    login_url = "login"

    def get_profile(self):
        '''returns the UserProfile for the currently logged-in user'''

        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                "name": self.request.user.username,
                "age": 0,
                "biography": "",
                "places_traveled": 0,
            },
        )
        return profile


class DestinationListView(ListView):
    """display all destinations and filter them by search or country."""
    model = Destination
    template_name = "project/destination_list.html"
    context_object_name = "destinations"

    def get_queryset(self):
        """return destinations filtered by the user's search inputs."""
        queryset = Destination.objects.all()

        search = self.request.GET.get("q")
        country = self.request.GET.get("country")

        if search:
            queryset = queryset.filter(name__icontains=search)

        if country:
            queryset = queryset.filter(country__name__icontains=country)

        return queryset

    def get_context_data(self, **kwargs):
        '''adds trip and bucket list summaries to the template context, including ISO country codes categorized by status visited,
        upcoming, wishlist for use in the interactive world map.'''
        context = super().get_context_data(**kwargs)

        all_trips = TripPlan.objects.all()
        today = timezone.now().date()
         # split trips into upcoming vs. completed based on travel date
        context["upcoming_trips"] = all_trips.filter(travel_date__gte=today)
        context["completed_trips"] = all_trips.filter(travel_date__lt=today)
        all_bucket_entries = BucketListEntry.objects.all()
        # separate active (not yet visited) from completed bucket list entries
        context["active_bucket_entries"] = all_bucket_entries.exclude(status="visited")
        context["completed_bucket_entries"] = all_bucket_entries.filter(
            status="visited"
        )
        # build lists of country codes grouped by map highlight category
        visited_codes = []
        upcoming_codes = []
        bucket_codes = []

        for trip in all_trips:
            code = trip.entry.destination.country.country_code

            if code:
                if trip.status == "completed":
                    visited_codes.append(code)
                else:
                    upcoming_codes.append(code)
        for entry in all_bucket_entries:
            code = entry.destination.country.country_code

            if code:
                if entry.status == "visited":
                    visited_codes.append(code)
                elif entry.status == "upcoming":
                    upcoming_codes.append(code)
                 # only show as wishlist if no trip has been planned for this entry
                elif not TripPlan.objects.filter(entry=entry).exists():
                    bucket_codes.append(code)
        # derrialize country code lists to JSON for use in JavaScript map rendering
        context["visited_codes"] = json.dumps(visited_codes)
        context["upcoming_codes"] = json.dumps(upcoming_codes)
        context["bucket_codes"] = json.dumps(bucket_codes)

        context["all_trips"] = all_trips
        context["all_bucket_entries"] = all_bucket_entries
        # preserve search inputs so the template can repopulate form fields
        context["search_query"] = self.request.GET.get("q", "")
        context["country_query"] = self.request.GET.get("country", "")
         # build a mapping of country code  detail URL for map click navigation
        country_links = {}

        for trip in all_trips:
            country = trip.entry.destination.country
            if country.country_code:
                country_links[country.country_code] = reverse(
                    "show_country", kwargs={"pk": country.pk}
                )

        for entry in all_bucket_entries:
            country = entry.destination.country
            if country.country_code:
                country_links[country.country_code] = reverse(
                    "show_country", kwargs={"pk": country.pk}
                )

        context["country_links"] = json.dumps(country_links)

        return context


class DestinationDetailView(DetailView):
    '''displays full details for a single destination, including any trip plans associated with it and a chronologically ordered potential itinerary.'''
    model = Destination
    template_name = "project/show_destination.html"
    context_object_name = "destination"

    def get_context_data(self, **kwargs):
        '''adds related trip plans and itinerary items for this destination to the template context.'''
        context = super().get_context_data(**kwargs)

        destination = self.object
        # fetch all trip plans that reference this destination via bucket list entries
        context["related_trips"] = TripPlan.objects.filter(
            entry__destination=destination
        )

        context["potential_itinerary_items"] = ItineraryItem.objects.filter(
            trip__entry__destination=destination
        ).order_by("day", "time")

        return context


class CountryDetailView(DetailView):
    ''''displays details for a country and all destinations within it.'''
    model = Country
    template_name = "project/show_country.html"
    context_object_name = "country"

    def get_context_data(self, **kwargs):
        ''' adds all destinations belonging to this country to the context.'''
        context = super().get_context_data(**kwargs)
        context["destinations"] = Destination.objects.filter(country=self.object)
        return context


class UserProfileListView(ListView):
    '''displays a list of all user profiles in the system.'''
    model = UserProfile
    template_name = "project/profile_list.html"
    context_object_name = "profiles"


class UserProfileDetailView(DetailView):
    '''displays a single user's profile along with their travel statistics nd a personal world map showing visited/upcoming/wishlist countries.'''
    model = UserProfile
    template_name = "project/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        '''computes per-user travel statistics (visited, upcoming, wishlist counts and total budget) and serializes country code data for the map widget.'''
        context = super().get_context_data(**kwargs)

        profile = self.object

        bucket_entries = BucketListEntry.objects.filter(user=profile)
        trip_plans = TripPlan.objects.filter(user=profile)
        # categorize country codes by travel status for map coloring
        visited_codes = []
        upcoming_codes = []
        bucket_codes = []

        for trip in trip_plans:
            code = trip.entry.destination.country.country_code

            if code:
                if trip.status == "completed":
                    visited_codes.append(code)
                else:
                    upcoming_codes.append(code)

        for entry in bucket_entries:
            code = entry.destination.country.country_code

            if code:
                if entry.status == "visited":
                    visited_codes.append(code)
                 # only mark as wishlist if no trip plan exists for this entry
                elif entry.status == "upcoming":
                    upcoming_codes.append(code)
                elif not TripPlan.objects.filter(entry=entry).exists():
                    bucket_codes.append(code)
         # serialize country code lists to JSON for JavaScript map rendering
        context["visited_codes"] = json.dumps(visited_codes)
        context["upcoming_codes"] = json.dumps(upcoming_codes)
        context["bucket_codes"] = json.dumps(bucket_codes)
        # use sets to avoid double-counting the same country across multiple trips/entries
        context["visited_count"] = len(set(visited_codes))
        context["upcoming_count"] = len(set(upcoming_codes))
        context["wishlist_count"] = len(set(bucket_codes))
        # sum budgets across all of this user's trip plans
        context["total_budget"] = sum(trip.budget for trip in trip_plans)
        # build country code detail URL mapping for map interactivity
        country_links = {}

        for trip in trip_plans:
            country = trip.entry.destination.country
            if country.country_code:
                country_links[country.country_code] = reverse(
                    "show_country", kwargs={"pk": country.pk}
                )

        for entry in bucket_entries:
            country = entry.destination.country
            if country.country_code:
                country_links[country.country_code] = reverse(
                    "show_country", kwargs={"pk": country.pk}
                )

        context["country_links"] = json.dumps(country_links)

        return context


class BucketListEntryListView(ProjectAuthMixin, ListView):
    '''displays the current user's bucket list entries with each entry annotated with its associated trip plan.'''
    model = BucketListEntry
    template_name = "project/bucket_list.html"
    context_object_name = "bucket_entries"

    def get_queryset(self):
        '''returns only the logged-in user's bucket list entries attaching the first related trip plan to each entry for
        convenient template access.'''
        entries = BucketListEntry.objects.filter(user=self.get_profile())

        for entry in entries:
            entry.trip = TripPlan.objects.filter(entry=entry).first()

        return entries


class BucketListEntryForm(forms.ModelForm):
    '''modelform for creating or editing a BucketListEntry. widget definitions used for styling.'''
    class Meta:
        model = BucketListEntry
        fields = ["destination", "priority", "status", "notes"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:10px;"
                }
            ),
            "country": forms.Select(
                attrs={
                    "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:10px;"
                }
            ),
            "continent": forms.TextInput(
                attrs={
                    "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:10px;"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; min-height:120px; margin-bottom:10px;"
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={"style": "margin-top:8px; margin-bottom:10px;"}
            ),
            "country_code": forms.TextInput(
                attrs={
                    "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:10px;"
                }
            ),
        }

class BucketListEntryCreateView(ProjectAuthMixin, CreateView):
    '''allows the logged-in user to add a destination to their bucket list. prevents duplicate entries for the same destination.'''
    model = BucketListEntry
    form_class = BucketListEntryForm
    template_name = "project/create_bucket.html"

    def form_valid(self, form):
        '''associates the new entry with the current user and the destination specified in the URL redirects back with an error if a duplicate exists.'''
        destination = Destination.objects.get(pk=self.kwargs["destination_pk"])
        user = self.get_profile()
        # against adding the same destination to the bucket list twice
        if BucketListEntry.objects.filter(user=user, destination=destination).exists():
            messages.error(
                self.request, "This destination is already in your bucket list."
            )
            return redirect(self.request.path)

        form.instance.user = user
        form.instance.destination = destination
        return super().form_valid(form)

    def get_form(self, form_class=None):
        '''applies consistent inline styling to all form fields.'''
        form = super().get_form(form_class)

        for field in form.fields:
            form.fields[field].widget.attrs.update(
                {
                    "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; font-size:15px; margin-bottom:14px;"
                }
            )

        return form

    def get_success_url(self):
        '''redirects to the bucket list page after a successful save.'''
        return reverse("bucket_list")

    def get_initial(self):
        '''pre-populates the destination field with the destination from the URL so the user can see which destination they're adding.'''
        initial = super().get_initial()
        initial["destination"] = Destination.objects.get(
            pk=self.kwargs["destination_pk"]
        )
        return initial


class BucketListEntryUpdateView(ProjectAuthMixin, UpdateView):
    '''allows the logged-in user to edit an existing bucket list entry they own.'''
    model = BucketListEntry
    template_name = "project/update_bucket.html"
    fields = ["destination", "priority", "status", "notes"]

    def get_queryset(self):
        '''restricts editing to entries belonging to the current user."'''
        return BucketListEntry.objects.filter(user=self.get_profile())

    def get_success_url(self):
        '''redirects to the bucket list page after a successful update.'''
        return reverse("bucket_list")

    def get_form(self, form_class=None):
        '''applies consistent inline styling to all form fields.'''
        form = super().get_form(form_class)

        for field in form.fields:
            form.fields[field].widget.attrs.update(
                {
                    "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; font-size:15px; margin-bottom:14px;"
                }
            )

        return form


class BucketListEntryDeleteView(ProjectAuthMixin, DeleteView):
    '''allows the logged-in user to delete an entry from their bucket list.'''
    model = BucketListEntry
    template_name = "project/delete_bucket.html"

    def get_queryset(self):
        '''restricts deletion to entries belonging to the current user.'''
        return BucketListEntry.objects.filter(user=self.get_profile())

    def get_success_url(self):
        '''redirects to the bucket list page after a successful deletion.'''
        return reverse("bucket_list")


class TripPlanListView(ProjectAuthMixin, ListView):
    '''displays all trip plans belonging to the currently logged-in user.'''
    model = TripPlan
    template_name = "project/trip_list.html"
    context_object_name = "trips"

    def get_queryset(self):
        '''returns only the current user's trip plans.'''
        return TripPlan.objects.filter(user=self.get_profile())


class TripPlanCreateView(ProjectAuthMixin, CreateView):
    '''allows the logged-in user to create a trip plan for one of their existing bucket list entries.'''
    model = TripPlan
    template_name = "project/create_trip.html"
    fields = ["travel_date", "budget", "status", "notes"]

    def get_context_data(self, **kwargs):
        '''passes the target bucket list entry to the template so the user can see which destination they are planning a trip for.'''
        context = super().get_context_data(**kwargs)
        entry = BucketListEntry.objects.get(
            pk=self.kwargs["entry_pk"], user=self.get_profile()
        )
        context["entry"] = entry
        return context

    def form_valid(self, form):
        '''associates the new trip plan with the current user and the bucket list entry specified in the URL.'''
        entry = BucketListEntry.objects.get(
            pk=self.kwargs["entry_pk"], user=self.get_profile()
        )
        form.instance.user = self.get_profile()
        form.instance.entry = entry
        return super().form_valid(form)

    def get_success_url(self):
        '''redirects to the trip list page after a successful save.'''
        return reverse("trips")


class TripPlanUpdateView(ProjectAuthMixin, UpdateView):
    '''allows the logged-in user to edit one of their existing trip plans.'''
    model = TripPlan
    template_name = "project/update_trip.html"
    fields = ["travel_date", "budget", "status", "notes"]

    def get_queryset(self):
        '''restricts editing to trip plans belonging to the current user.'''
        return TripPlan.objects.filter(user=self.get_profile())

    def get_success_url(self):
        '''redirects to the trip list page after a successful update.'''
        return reverse("trips")


class TripPlanDeleteView(ProjectAuthMixin, DeleteView):
    '''allows the logged-in user to delete one of their trip plans.'''
    model = TripPlan
    template_name = "project/delete_trip.html"

    def get_queryset(self):
        '''restricts deletion to trip plans belonging to the current user.'''
        return TripPlan.objects.filter(user=self.get_profile())

    def get_form(self, form_class=None):
        ''' applies consistent inline styling to all form fields.'''
        form = super().get_form(form_class)

        for field in form.fields:
            form.fields[field].widget.attrs.update(
                {
                    "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; font-size:15px; margin-bottom:14px;"
                }
            )

        return form

    def get_success_url(self):
        '''redirects to the trip list page after a successful deletion.'''
        return reverse("trips")


class CommentCreateView(ProjectAuthMixin, CreateView):
    '''allows the logged-in user to post a comment on a specific destination.'''
    model = Comment
    template_name = "project/create_comment.html"
    fields = ["text"]

    def get_context_data(self, **kwargs):
        '''passes the destination being commented on to the template so it can be displayed alongside the form.'''
        context = super().get_context_data(**kwargs)
        context["destination"] = Destination.objects.get(
            pk=self.kwargs["destination_pk"]
        )
        return context

    def get_form(self, form_class=None):
        '''replaces the default text widget with a styled text area that includes placeholder copy and removes the field label.'''
        form = super().get_form(form_class)
        form.fields["text"].widget = forms.Textarea(
            attrs={
                "placeholder": "Share your thoughts, travel tips, experiences, or recommendations...",
                "style": "width:100%; min-height:210px; padding:16px; border-radius:12px; border:1px solid #cbd5e1; font-size:15px; resize:vertical;",
            }
        )
        form.fields["text"].label = ""
        return form

    def form_valid(self, form):
        '''associates the comment with the current user and the destination from the URL before saving.'''
        form.instance.user = self.get_profile()
        form.instance.destination = Destination.objects.get(
            pk=self.kwargs["destination_pk"]
        )
        return super().form_valid(form)

    def get_success_url(self):
        '''redirects back to the destination detail page after posting.'''
        return reverse("show_destination", kwargs={"pk": self.kwargs["destination_pk"]})


class ItineraryCreateView(ProjectAuthMixin, CreateView):
    '''allows the logged-in user to add a new itinerary item to one of their trip plans.'''
    model = ItineraryItem
    template_name = "project/create_itinerary.html"
    fields = ["day", "time", "activity", "location", "notes"]

    def form_valid(self, form):
        '''associates the new itinerary item with the trip plan specified in the URL verifying the trip belongs to the current user.'''
        trip = TripPlan.objects.get(pk=self.kwargs["trip_pk"], user=self.get_profile())
        form.instance.trip = trip
        return super().form_valid(form)

    def get_success_url(self):
        '''redirects to the trip list page after a successful save.'''
        return reverse("trips")


class DestinationRatingCreateView(ProjectAuthMixin, CreateView):
    '''allows the logged-in user to submit a 1–10 rating and written review for a specific destination.'''
    model = DestinationRating
    template_name = "project/create_rating.html"
    fields = ["rating", "review"]

    def form_valid(self, form):
        '''associates the rating with the current user and the destination from the URL before saving.'''
        form.instance.user = self.get_profile()
        form.instance.destination = Destination.objects.get(
            pk=self.kwargs["destination_pk"]
        )
        return super().form_valid(form)

    def get_form(self, form_class=None):
        '''replaces the rating field with a 1–10 dropdown and applies consistent styling to the review textarea.'''
        form = super().get_form(form_class)

        form.fields["rating"].widget = forms.Select(
            choices=[(i, i) for i in range(1, 11)],
            attrs={
                "style": "width:100%; height:48px; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:14px; font-size:15px; background:white;"
            },
        )

        form.fields["review"].widget.attrs.update(
            {
                "style": "width:100%; min-height:130px; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:14px; font-size:15px;"
            }
        )

        return form

    def get_success_url(self):
        '''redirects back to the destination detail page after submitting'''
        return reverse("show_destination", kwargs={"pk": self.kwargs["destination_pk"]})


class DestinationCreateView(ProjectAuthMixin, CreateView):
    '''allows the logged-in user to create a new destination and associate it with an existing country.'''
    model = Destination
    template_name = "project/create_destination.html"
    fields = ["name", "country", "description", "image"]

    def get_form(self, form_class=None):
        '''applies consistent inline styling to all form fields'''
        form = super().get_form(form_class)

        form.fields["name"].widget.attrs.update(
            {
                "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:14px; font-size:15px;"
            }
        )

        form.fields["country"].widget.attrs.update(
            {
                "style": "width:100%; height:48px; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:14px; font-size:15px; background:white;"
            }
        )

        form.fields["description"].widget.attrs.update(
            {
                "style": "width:100%; min-height:130px; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:14px; font-size:15px;"
            }
        )

        form.fields["image"].widget.attrs.update(
            {"style": "margin-top:10px; margin-bottom:20px;"}
        )

        return form

    def get_success_url(self):
        '''redirects to the destinations list page after a successful save.'''
        return reverse("destinations")


class CountryCreateView(ProjectAuthMixin, CreateView):
    '''allows the logged-in user to create a new country entry, including its ISO country code for use in the world map widget.'''
    model = Country
    template_name = "project/create_country.html"
    fields = ["name", "continent", "description", "image", "country_code"]

    def get_form(self, form_class=None):
        '''replaces default widgets with styled versions and adds a placeholder hint for the country code field.'''
        form = super().get_form(form_class)

        form.fields["name"].widget = forms.TextInput(
            attrs={
                "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:14px; font-size:15px;"
            }
        )

        form.fields["continent"].widget = forms.TextInput(
            attrs={
                "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:14px; font-size:15px;"
            }
        )

        form.fields["description"].widget = forms.Textarea(
            attrs={
                "style": "width:100%; min-height:130px; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:14px; font-size:15px;"
            }
        )

        form.fields["country_code"].widget = forms.TextInput(
            attrs={
                "placeholder": "Example: US, FR, JP",
                "style": "width:100%; padding:12px; border-radius:10px; border:1px solid #cbd5e1; margin-bottom:14px; font-size:15px;",
            }
        )

        return form

    def get_success_url(self):
        '''redirects to the create destination page after saving'''
        return reverse("create_destination")


class ItineraryItemDelete(ProjectAuthMixin, DeleteView):
    '''allows the logged-in user to delete an individual itinerary item.'''
    model = ItineraryItem
    template_name = "project/delete_itinerary.html"

    def get_success_url(self):
        '''redirects to the trip list page after a successful deletion.'''
        return reverse("trips")


class MyProfileView(ProjectAuthMixin, View):
    '''view that redirects the logged-in user to their own profile page without requiring them to know their profile's primary key.'''
    def get(self, request):
        profile = self.get_profile()
        return redirect("show_profile", pk=profile.pk)


class CountryDetailView(DetailView):
    '''Displays details for a country and all destinations within it.'''
    model = Country
    template_name = "project/show_country.html"
    context_object_name = "country"

    def get_context_data(self, **kwargs):
        '''adds all destinations belonging to this country to the context.'''
        context = super().get_context_data(**kwargs)
        context["destinations"] = Destination.objects.filter(country=self.object)
        return context
