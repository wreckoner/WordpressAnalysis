from django.shortcuts import render
from models import Wordpress
from common.analyzer import Analysis
from django.core.serializers.json import DjangoJSONEncoder
import json, datetime

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
	'footer' : datetime.datetime.now().year
	}
	return render(requests, template, context)


def stats(requests):
	template = 'tuftsWPA_stats.html'
	url, level = requests.GET['url'], requests.GET['level']
	if level == 'page':
		template = 'page_stat.html'
	db_object = Wordpress.objects.filter(url = url)[0]
	page_label = '. '.join([db_object.title, db_object.subtitle])
	sub_pages = None
	word_count = None
	word_count_json = None
	word_bags = None
	if level == 'site':
		header = ''.join(['Statistics of the site - ', page_label])
		sub_pages = Wordpress.objects.filter(parent=url)
	else:
		header = 'Page Statistics'
		word_count, word_bags = Analysis(db_object.content).word_counter()
		word_count = [[k.capitalize().encode('ascii', 'ignore'), word_count[k]] for k in word_count]
		word_count.sort(key=lambda x:x[1], reverse=True)
		word_count_json = json.dumps(word_count, cls=DjangoJSONEncoder) 
	context = {
	'title' : 'Tufts Wordpress Analysis',
	'header' : header,
	'level' : level,
	'db_object' : db_object,
	'sub_pages' : sub_pages,
	'word_count' : word_count,
	'word_bags' : word_bags,
	'word_count_json' : word_count_json,
	'footer' : datetime.datetime.now().year
	}
	return render(requests, template, context)