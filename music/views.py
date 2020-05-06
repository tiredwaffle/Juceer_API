from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import CharField, Value

from music.models import MusicPost
from music.serializers import MusicSerializer

from searches.models import SearchQuery

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser,FileUploadParser 
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import generics
from rest_framework_csv.renderers import CSVRenderer

import csv
import json
import statistics

from django.views.generic import View
from django.http import HttpResponse


class music_list(APIView):
    renderer_classes = [JSONRenderer,CSVRenderer, TemplateHTMLRenderer]
    template_name = 'music/list_artist.html'

    def get(self, request, format = None):
        music = MusicPost.objects.order_by('artist_name').values('artist_id', 'artist_name', 'artist_info').distinct()
        title = "List of artists"
        serializer = MusicSerializer(music, many=True)
        return Response({'object_list': serializer.data,  'title': title})

    def post(self, request, format = None):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class music_pop_list(APIView):
    renderer_classes = [JSONRenderer,CSVRenderer, TemplateHTMLRenderer]
    template_name = 'music/list_artist.html'
    
    def get(self, request, number = None, format = None):
        if (int(number) == 0):
            raise Http404
        music = MusicPost.objects.order_by('artist_hotttnesss').reverse().values('artist_id', 'artist_name', 'artist_info').distinct()
        title = "List of artists by popularity"
        if (number == None):
            serializer = MusicSerializer(music, many=True)
        else:
            serializer = MusicSerializer(music[:int(number)], many=True)
        return Response({'object_list': serializer.data,  'title': title})

    def post(self, request, format = None):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class music_detail(APIView):
    """
    Retrieve, update or delete a code music.
    """
    renderer_classes = [JSONRenderer, CSVRenderer ,TemplateHTMLRenderer]
    template_name = 'music/detail_artist.html'

    def get_object(self, artist_id):
        try:
            music = MusicPost.objects.get(artist_id = artist_id)
        except MusicPost.DoesNotExist:
            raise Http404

    def get(self, request, artist_id, format = None):
        #music = MusicPost.objects.get(artist_id = artist_id)
        music = MusicPost.objects.filter(artist_id = artist_id).values("artist_hotttnesss", "artist_id", "artist_name", "artist_terms").all()
        if (len(music)==0):
            raise Http404
        serializer = MusicSerializer(music[0])
        context = {
        "object": serializer.data,
        "songs_of_the_artist": 'http://127.0.0.1:8000/juceer/0.1/artists/' + str(artist_id) + '/songs/',
        "statistic_of_the_artist": 'http://127.0.0.1:8000/juceer/0.1/statistics/mean/artists/' + str(artist_id) + '/',
        }
        return Response(context)
        
    def put(self, request, artist_id, format = None):
        music = self.get_object(artist_id)
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class music_year_list(APIView):
    renderer_classes = [JSONRenderer,CSVRenderer, TemplateHTMLRenderer]
    template_name = 'music/list_artist.html'
    
    def get(self, request, format = None):
        music = MusicPost.objects.order_by('song_year').reverse().values('song_year').distinct()
        title = "List of years"
        serializer = MusicSerializer(music, many=True)
        return Response({'object_list': serializer.data, 'link':"/juceer/0.1/artists/years/", 'title': title, 'song_year': song_year})

    def post(self, request, format = None):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class songs_list(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer, TemplateHTMLRenderer]
    template_name = 'music/list_song.html'

    def get(self, request, artist_id = None, song_year = None, format = None):
        #music = MusicPost.objects.all()
        if (artist_id == None or song_year == None):
            music = MusicPost.objects.order_by('song_hotttnesss').reverse().all()
            title = "List of songs"
        elif(artist_id != None and song_year != None):
            music = MusicPost.objects.filter(artist_id = artist_id, song_year = song_year).all()
            if(len(music)==0):
                raise Http404
            title = "List of songs of "+ music[0].artist_name + " in " + song_year
        serializer = MusicSerializer(music, many=True)
        return Response({'object_list': serializer.data,  'title': title })

    def post(self, request, format = None):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #serializer_class = MusicSerializer

class song_detail(APIView):
    """
    Retrieve, update or delete a code music.
    """
    renderer_classes = [JSONRenderer,  CSVRenderer, TemplateHTMLRenderer]
    template_name = 'music/detail_song.html'

    def get_object(self, song_id):
        try:
            music = MusicPost.objects.get(song_id = song_id)
        except MusicPost.DoesNotExist:
            raise Http404

    def get(self, request, song_id, format = None):
        #music = MusicPost.objects.get(artist_id = artist_id)
        music = MusicPost.objects.filter(song_id = song_id).all()
        if (len(music)==0):
            raise Http404
        serializer = MusicSerializer(music[0])
        context = {
        "object": serializer.data,
        "songs_of_the_same_year": 'http://127.0.0.1:8000/juceer/0.1/years/'+ str(music[0].song_year) + '/',
        "songs_of_the_same_artist": 'http://127.0.0.1:8000/juceer/0.1/artists/' + str(music[0].artist_id) + '/songs/',
        "artists_of_the_same_ganre": 'http://127.0.0.1:8000/juceer/0.1/genres/' + str(music[0].artist_terms) + '/artists/',
        "google_artist": 'https://www.google.com/?q=' + music[0].artist_name + '/',
        }
        return Response(context)
        
    def put(self, request, song_id, format = None):
        music = self.get_object(song_id)
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete (self, request, song_id, format = None):
        music = MusicPost.objects.filter(song_id = song_id).all()
        music.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class songs_pop_year_list(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'music/list_song.html'
    
    def get(self, request, number = None, song_year= None, format = None):
        if (int(number) == 0):
            raise Http404
        if (number == None or song_year == None):
            raise Http404
        elif(number != None and song_year != None):
            music = MusicPost.objects.filter(song_year = song_year).order_by('artist_hotttnesss').reverse().values('artist_id', 'artist_name', 'artist_info', 'song_id').distinct()
            title = "List of songs by popularity in "+song_year
            serializer = MusicSerializer(music, many=True)
        return Response({'object_list': serializer.data,  'title': title, 'song_year': song_year})

    def post(self, request, format = None):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class song_years_list(APIView):
    renderer_classes = [JSONRenderer,  CSVRenderer, TemplateHTMLRenderer]
    template_name = 'music/list_years.html'
    
    def get(self, request, format = None):
        music = MusicPost.objects.order_by('song_year').reverse().values('song_year').distinct()
        title = "List of songs by years"
        serializer = MusicSerializer(music, many=True)
        return Response({'object_list': serializer.data,  'title': title})

    def post(self, request, format = None):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class genre_list(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer,  TemplateHTMLRenderer]
    template_name = 'music/list_genre.html'

    def get(self, request, format = None):
        music = MusicPost.objects.order_by('artist_terms').values('artist_terms').distinct()
        title = "List of genres"
        serializer = MusicSerializer(music, many=True)
        return Response({'object_list': serializer.data,  'title': title })

    def post(self, request, format = None):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class artist_genre_list(APIView):
    renderer_classes = [JSONRenderer,  CSVRenderer, TemplateHTMLRenderer]
    template_name = 'music/list_artist.html'

    def get(self, request, artist_terms = None, format = None):
        music = MusicPost.objects.filter(artist_terms = artist_terms).order_by('artist_name').values("artist_id", "artist_name", "artist_info").distinct()
        if (len(music)==0):
            raise Http404
        title = "List of artists of "+ artist_terms.replace("_", " ") + " genre"
        serializer = MusicSerializer(music, many=True)
        return Response({'object_list': serializer.data,  'title': title })

    def post(self, request, format = None):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class stat_mean(APIView):

    renderer_classes = [JSONRenderer,  CSVRenderer, TemplateHTMLRenderer]
    template_name = 'music/stat_artist.html'

    def get_object(self, song_id):
        try:
            music = MusicPost.objects.get(song_id = song_id)
        except MusicPost.DoesNotExist:
            raise Http404

    def get(self, request, artist_id = None, format = None):
        if (artist_id == None):
            raise Http404
        music = list(MusicPost.objects.filter(artist_id = artist_id).values_list('song_hotttnesss', flat=True))
        if (len(music)==0):
            raise Http404
        list_year = list(MusicPost.objects.filter(artist_id = artist_id).values_list('song_year', flat=True).distinct())

        serializer = MusicSerializer(music[0])
        artist_name = MusicPost.objects.filter(artist_id = artist_id).all()
        context = {
        "object": serializer.data,
        "mean": statistics.mean(music),
        "artist_name": artist_name[0].artist_name,
        "artist_id": artist_id,
        "stat": list_year,
        "median": 'http://127.0.0.1:8000/juceer/0.1/statistics/median/artists/'+ str(artist_id) + '/',
        "std_deviation": 'http://127.0.0.1:8000/juceer/0.1/statistics/std_dev/artists/'+ str(artist_id) + '/',
        "songs_of_the_same_artist": 'http://127.0.0.1:8000/juceer/0.1/artists/' + str(artist_id) + '/songs/',
        }

        return Response(context)
        
    def put(self, request, song_id, format = None):
        music = self.get_object(song_id)
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class stat_median(APIView):

    renderer_classes = [JSONRenderer,  CSVRenderer, TemplateHTMLRenderer]
    template_name = 'music/stat_artist.html'

    def get_object(self, song_id):
        try:
            music = MusicPost.objects.get(song_id = song_id)
        except MusicPost.DoesNotExist:
            raise Http404

    def get(self, request, artist_id = None, format = None):
        if (artist_id == None):
            raise Http404
        music = list(MusicPost.objects.filter(artist_id = artist_id).values_list('song_hotttnesss', flat=True))
        if (len(music)==0):
            raise Http404
        serializer = MusicSerializer(music[0])
        list_year = list(MusicPost.objects.filter(artist_id = artist_id).values_list('song_year', flat=True).distinct())
        context = {
        "object": serializer.data,
        "stat": list_year,
        "mean": 'http://127.0.0.1:8000/juceer/0.1/statistics/mean/artists/'+ str(artist_id) + '/',
        "median": statistics.median(music),
        "std_deviation": 'http://127.0.0.1:8000/juceer/0.1/statistics/std_dev/artists/'+ str(artist_id) + '/',
        "songs_of_the_same_artist": 'http://127.0.0.1:8000/juceer/0.1/artists/' + str(artist_id) + '/songs/',
        }

        return Response(context)
        
    def put(self, request, song_id, format = None):
        music = self.get_object(song_id)
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class stat_std_dev(APIView):

    renderer_classes = [JSONRenderer,  CSVRenderer, TemplateHTMLRenderer]
    template_name = 'music/stat_artist.html'

    def get_object(self, song_id):
        try:
            music = MusicPost.objects.get(song_id = song_id)
        except MusicPost.DoesNotExist:
            raise Http404

    def get(self, request, artist_id = None, format = None):
        if (artist_id == None):
            raise Http404
        qs = MusicPost.objects.filter(artist_id = artist_id).all()
        if (len(qs)==0):
            raise Http404
        music = list(MusicPost.objects.filter(artist_id = artist_id).values_list('song_hotttnesss', flat=True))
        numb = len(music)
        if(numb > 1):
            std_deviation = statistics.stdev(music)
        else:
            std_deviation = 0
        serializer = MusicSerializer(music[0])
        list_year = list(MusicPost.objects.filter(artist_id = artist_id).values_list('song_year', flat=True).distinct())
        context = {
        "object": serializer.data,
        "stat": list_year,
        "mean": 'http://127.0.0.1:8000/juceer/0.1/statistics/mean/artists/'+ str(artist_id) + '/',
        "median": 'http://127.0.0.1:8000/juceer/0.1/statistics/median/artists/'+ str(artist_id) + '/',
        "std_deviation": str(std_deviation),
        "songs_of_the_same_artist": 'http://127.0.0.1:8000/juceer/0.1/artists/' + str(artist_id) + '/songs/',
        }

        return Response(context)
        
    def put(self, request, song_id, format = None):
        music = self.get_object(song_id)
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class stat_mean_year(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer,  TemplateHTMLRenderer]
    template_name = 'music/stat_artist.html'

    def get_object(self, song_id):
        try:
            music = MusicPost.objects.get(song_id = song_id)
        except MusicPost.DoesNotExist:
            raise Http404

    def get(self, request, artist_id = None, song_year =  None, format = None):
        if (artist_id == None or song_year == None):
            raise Http404
        music = list(MusicPost.objects.filter(artist_id = artist_id).filter(song_year=song_year).values_list('song_hotttnesss', flat=True))
        if (len(music)==0):
            raise Http404
        list_year = list(MusicPost.objects.filter(artist_id = artist_id).values_list('song_year', flat=True).distinct())

        serializer = MusicSerializer(music[0])
        artist_name = MusicPost.objects.filter(artist_id = artist_id).all()
        context = {
        "object": serializer.data,
        "mean": statistics.mean(music),
        "artist_name": artist_name[0].artist_name,
        "artist_id": artist_id,
        "stat": list_year,
        "year": song_year,
        "median": 'http://127.0.0.1:8000/juceer/0.1/statistics/median/artists/'+ str(artist_id) + '/',
        "std_deviation": 'http://127.0.0.1:8000/juceer/0.1/statistics/std_dev/artists/'+ str(artist_id) + '/',
        "songs_of_the_same_artist": 'http://127.0.0.1:8000/juceer/0.1/artists/' + str(artist_id) + '/songs/',
        }

        return Response(context)
        
    def put(self, request, song_id, format = None):
        music = self.get_object(song_id)
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class stat_median_year(APIView):

    renderer_classes = [JSONRenderer,  CSVRenderer, TemplateHTMLRenderer]
    template_name = 'music/stat_artist.html'

    def get_object(self, song_id):
        try:
            music = MusicPost.objects.get(song_id = song_id)
        except MusicPost.DoesNotExist:
            raise Http404

    def get(self, request, artist_id = None, song_year=None, format = None):
        if (artist_id == None):
            raise Http404
        music = list(MusicPost.objects.filter(artist_id = artist_id).filter(song_year=song_year).values_list('song_hotttnesss', flat=True))
        if (len(music)==0):
            raise Http404
        serializer = MusicSerializer(music[0])
        artist_name = MusicPost.objects.filter(artist_id = artist_id).all()
        list_year = list(MusicPost.objects.filter(artist_id = artist_id).values_list('song_year', flat=True).distinct())
        context = {
        "object": serializer.data,
        "artist_name": artist_name[0].artist_name,
        "artist_id": artist_id,
        "stat": list_year,
        "year": song_year,
        "mean": 'http://127.0.0.1:8000/juceer/0.1/statistics/mean/artists/'+ str(artist_id) + '/',
        "median": statistics.median(music),
        "std_deviation": 'http://127.0.0.1:8000/juceer/0.1/statistics/std_dev/artists/'+ str(artist_id) + '/',
        "songs_of_the_same_artist": 'http://127.0.0.1:8000/juceer/0.1/artists/' + str(artist_id) + '/songs/',
        }

        return Response(context)
        
    def put(self, request, song_id, format = None):
        music = self.get_object(song_id)
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class stat_std_dev_year(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer,  TemplateHTMLRenderer]
    template_name = 'music/stat_artist.html'

    def get_object(self, song_id):
        try:
            music = MusicPost.objects.get(song_id = song_id)
        except MusicPost.DoesNotExist:
            raise Http404

    def get(self, request, artist_id = None, song_year=None, format = None):
        if (artist_id == None):
            raise Http404
        qs = MusicPost.objects.filter(artist_id = artist_id).all()
        if (len(qs)==0):
            raise Http404
        music = list(MusicPost.objects.filter(artist_id = artist_id).filter(song_year=song_year).values_list('song_hotttnesss', flat=True))
        numb = len(music)
        if(numb > 1):
            std_deviation = statistics.stdev(music)
        else:
            std_deviation = 0
        serializer = MusicSerializer(music[0])
        artist_name = MusicPost.objects.filter(artist_id = artist_id).all()
        list_year = list(MusicPost.objects.filter(artist_id = artist_id).values_list('song_year', flat=True).distinct())
        context = {
        "object": serializer.data,
        "artist_name": artist_name[0].artist_name,
        "artist_id": artist_id,
        "stat": list_year,
        "year": song_year,
        "mean": 'http://127.0.0.1:8000/juceer/0.1/statistics/mean/artists/'+ str(artist_id) + '/',
        "median": 'http://127.0.0.1:8000/juceer/0.1/statistics/median/artists/'+ str(artist_id) + '/',
        "std_deviation": str(std_deviation),
        "songs_of_the_same_artist": 'http://127.0.0.1:8000/juceer/0.1/artists/' + str(artist_id) + '/songs/',
        }

        return Response(context)
        
    def put(self, request, song_id, format = None):
        music = self.get_object(song_id)
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MusicCSVExportView(View):

    serializer_class = MusicSerializer
    
    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        
        serializer = self.get_serializer(
            MusicPost.objects.all(),
            many=True
        )
        header = MusicSerializer.Meta.fields
        
        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)
        
        return response

class MusicCSImportView(View):
    #MusicPost.objects.all().delete()
    def get(self, request):
        CSV_PATH = 'C:/Users/yulyz/Downloads/music1000.csv'           #change path here!!!!!!!!
        with open(CSV_PATH, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            k = spamreader.__next__()
            for column in spamreader:
                #print(column[1])
                MusicPost.objects.create(
                    artist_hotttnesss = float(column[1]),
                    artist_id = column[2],
                    artist_name = column[6],
                    artist_terms = column[8].replace(" ","_"),
                    release_id = column[10],
                    song_hotttnesss= float(column[20]),
                    song_id = column[21],
                    song_year = float(column[34]),
                    song_info = 'http://127.0.0.1:8000/juceer/0.1/songs/' + str(column[21]) + '/',
                    artist_info = 'http://127.0.0.1:8000/juceer/0.1/artists/' + str(column[2]) + '/'
                    )
        return HttpResponse('Dataset uploaded')

    def post(self,request):
        return HttpResponse('Class post based view')


class SearchView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer,  TemplateHTMLRenderer]
    template_name = 'music/list_song.html'

    def get(self, request):
        query = request.GET.get('q', None)
        user = None
        context = {"query": query}
        title = 'You searched for '+ query
        if query:   
            SearchQuery.objects.create(user = user, query = query)
            s_list = MusicPost.objects.filter(artist_name__icontains = str(query)).all()|MusicPost.objects.filter(artist_terms__icontains = str(query)).all()|MusicPost.objects.filter(song_year__icontains = str(query))
            s_list = s_list.order_by('artist_name').all()
            context["s_list"] = s_list
        else:
            title = "You search is empty"
            s_list = []
        serializer = MusicSerializer(s_list, many = True)
        return Response({'object_list': serializer.data , "title": title})