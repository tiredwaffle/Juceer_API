from django.db import models
from django.conf import settings
from django.utils import crypto

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

User = settings.AUTH_USER_MODEL


class MusicPostQuerySet(models.QuerySet):
	def published(self):
		now = timezone.now()
		return self.filter(publish_date__lte = now)
	def search(self,query):
		return self.filter(title__iexact = query)

class MusicPostManager(models.Manager):
	def get_queryset(self):
		return MusicPostQuerySet(self.model, using = self._db)
	
	def published(self):
		return self.get_queryset().published()

	def search(self, query = None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().search(query)


class MusicPost(models.Model):
	song_id = models.SlugField(unique = True, default = crypto.get_random_string(length = 17))
	artist_hotttnesss= models.FloatField(default = 0)
	artist_id = models.CharField(max_length=100, default = crypto.get_random_string(length = 17))
	artist_name = models.CharField(max_length=100, default = crypto.get_random_string(length = 5))
	artist_terms = models.CharField(max_length=100, default = crypto.get_random_string(length = 5))
	release_id = models.IntegerField(default = 0)
	song_hotttnesss= models.FloatField(default = 0)
	song_year = models.IntegerField(default = 0)
	song_info = models.CharField(max_length=100, default = '/')
	artist_info = models.CharField(max_length=100, default = '/')