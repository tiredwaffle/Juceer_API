from django.http import HttpResponse 
from django.shortcuts import render
from django.template.loader import get_template


def home_page(request):						# home page
	my_title = "We are happy to see you here!"
	context ={"title": my_title}
	return render (request, "home.html", context)
