from django.urls import path
from music import views
from rest_framework.urlpatterns import format_suffix_patterns

from searches.views import search_view

urlpatterns = [
    path('artists/', 							views.music_list.as_view()),
    path('artists/years/',                      views.music_year_list.as_view()),
    path('artists/hottest/<str:number>/', 		views.music_pop_list.as_view()),
    path('artists/<str:artist_id>/', 			views.music_detail.as_view()),
    path('artists/<str:artist_id>/songs/',	 	views.songs_list.as_view()),
    path('artists/<str:artist_id>/songs/year/<str:song_year>/',	 	views.songs_list.as_view()),
    
    path('songs/', 								views.songs_list.as_view()),
    path('songs/years/',                        views.song_years_list.as_view()),
    path('songs/years/<str:song_year>/hottest/<str:number>/',       views.songs_pop_year_list.as_view()),
    path('songs/<str:song_id>/',               views.song_detail.as_view()),
    
    path('genres/', 							views.genre_list.as_view()),
    path('genres/<str:artist_terms>/artists/', 	views.artist_genre_list.as_view()),

    path('statistics/mean/artists/<str:artist_id>/years/<str:song_year>/', views.stat_mean_year.as_view()),
    path('statistics/median/artists/<str:artist_id>/years/<str:song_year>/', views.stat_median_year.as_view()),
    path('statistics/std_dev/artists/<str:artist_id>/years/<str:song_year>/', views.stat_std_dev_year.as_view()),



    path('statistics/mean/artists/<str:artist_id>/', views.stat_mean.as_view()),
    path('statistics/median/artists/<str:artist_id>/', views.stat_median.as_view()),
    path('statistics/std_dev/artists/<str:artist_id>/', views.stat_std_dev.as_view()),

    path('upload/', 							views.MusicCSImportView.as_view()),
    path('download/',							views.MusicCSVExportView.as_view()),
    path('search/',                             views.SearchView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)