from django.shortcuts import render
from models import Wordpress
from common.analyzer import Analysis

# Create your views here.

def home(requests):
	'''Handler for the root/home page of the Wordpress Analysis Project.'''
	template = 'tuftsWPA.html'
	db_object = Wordpress.objects.filter(level='root')[0]
	sites = Wordpress.objects.filter(level='site')
	context = {
	'title' : 'Tufts WordPress Analysis',
	'header' : 'Tufts Wordpress Analysis (WPA) Project',
	'message' : 'This is the main page of the WPA project. Below you can find the latest activity in various Tufts Wordpress Sites...',
	'db_object' : db_object,
	'sites' : sites,
	'site_count' : len(sites),
	}
	return render(requests, template, context)


def stats(requests):
	template = 'tuftsWPA_stats.html'
	url, level = requests.GET['url'], requests.GET['level']
	db_object = Wordpress.objects.filter(url = url)[0]
	page_label = '. '.join([db_object.title, db_object.subtitle])
	sub_pages = None
	word_count = None
	if level == 'site':
		header = ''.join(['Statistics of the site - ', page_label])
		sub_pages = Wordpress.objects.filter(parent=url)
	else:
		header = ''.join(['Statistics of the page - ', page_label])
		word_count = Analysis(db_object.content).word_counter()
	context = {
	'title' : 'Tufts Wordpress Analysis',
	'header' : header,
	'level' : level,
	'db_object' : db_object,
	'sub_pages' : sub_pages,
	'word_count' : word_count,
	}
	return render(requests, template, context)