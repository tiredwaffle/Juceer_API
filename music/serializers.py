from rest_framework import serializers
from music.models import MusicPost
from django.utils import crypto

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicPost
        fields = ['song_id', 'artist_hotttnesss', 'artist_id', 'artist_name', 'artist_terms', 'release_id', 'song_hotttnesss', 'song_year', 'song_info', 'artist_info']

    def create(self, reques, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """

        return MusicPost.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.song_id = validated_data.get('song_id', instance.song_id) 
        instance.artist_hotttnesss = validated_data.get('artist_hotttnesss', instance.artist_hotttnesss) 
        instance.artist_id = validated_data.get('artist_id', instance.artist_id) 
        instance.artist_name = validated_data.get('artist_name', instance.artist_name) 
        instance.artist_terms = validated_data.get('artist_terms', instance.artist_terms) 
        instance.release_id = validated_data.get('release_id', instance.release_id) 
        instance.song_hotttnesss = validated_data.get('song_hotttnesss', instance.song_hotttnesss) 
        instance.song_year = validated_data.get('song_year', instance.song_year) 
        instance.song_info = validated_data.get('song_info', instance.song_info) 
        instance.artist_info = validated_data.get('artist_info', instance.artist_info) 
        instance.save()
        return instance