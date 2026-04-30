from django.contrib import admin

# Register your models here.
from .models import UserProfile, Country, Destination, BucketListEntry, TripPlan, Comment

admin.site.register(UserProfile)
admin.site.register(Country)
admin.site.register(Destination)
admin.site.register(BucketListEntry)
admin.site.register(TripPlan)
admin.site.register(Comment)