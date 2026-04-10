# File: serializers.py
# Author: Esha Wadher (eshaaw@bu.edu), 4/9/2026
# Description: Serializers for the mini_insta REST API, converting
# model instances to/from JSON format.

from rest_framework import serializers
from .models import Profile, Post, Photo

class PhotoSerializer(serializers.ModelSerializer):
    '''aerializer to convert Photo objects to from JSON.'''
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image_url', 'image_file', 'image', 'timestamp']

    def get_image(self, obj):
        '''return the best available image URL.'''
        request = self.context.get('request')
        url = obj.get_image_url()
        if url and request:
            return request.build_absolute_uri(url)
        return url

class PostSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True, source='get_all_photos')
    profile_username = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'profile', 'profile_username', 'profile_image',
                  'caption', 'timestamp', 'photos']
        # no image_url here!

    def get_profile_username(self, obj):
        '''return the username of the post profile.'''
        return obj.profile.username

    def get_profile_image(self, obj):
        '''return the profile image URL.'''
        return obj.profile.profile_image_url

class ProfileSerializer(serializers.ModelSerializer):
    '''serializer to convert Profile objects to/from JSON.'''

    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url',
                  'bio_text', 'join_date']