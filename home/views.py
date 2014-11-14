from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(requests):
	template = 'home.html'
	context = {
	'title' : 'My Projects',
	'header' : '',
	'message' : 'Click on one of the links below to go to the respective project page.',
	'links' : [{'name': 'Tufts Wordpress Analysis (WPA) Project', 'url': '/wordpress/'}]
	}
	#return render(requests, template, context)
	return HttpResponse("Hello World")