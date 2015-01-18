from django.shortcuts import render
from models import Wordpress
from common.analyzer import Analysis
from django.core.serializers.json import DjangoJSONEncoder
import json, datetime, pprint

# Create your views here.

def home(requests):
	'''Handler for the root/home page of the Wordpress Analysis Project.'''
	template = 'tuftsWPA.html'
	template = 'root_stat.html'
	db_object = Wordpress.objects.filter(level='root')[0]
	sites = Wordpress.objects.filter(level='site')
	site_tree = {'url' : db_object.url, 'title' : db_object.title, 'subtitle' : db_object.subtitle, 'published' : db_object.published, 'level' : db_object.level, 'children' : []}
	site_tree['children'] = [{'url' : site.url, 'title' : site.title, 'subtitle' : site.subtitle, 'published' : site.published, 'level' : site.level, 'children' : []} for site in sites]
	# for site in site_tree['children']:
	# 	temp = [{'url' : post.url, 'title' : post.title, 'subtitle' : post.subtitle, 'published' : post.published, 'level' : post.level} for post in Wordpress.objects.filter(parent=site['url'])]
	# 	site['children'] = temp
	context = {
	'title' : 'Tufts WordPress Analysis',
	'header' : 'Tufts Wordpress Analysis (WPA) Project',
	'db_object' : db_object,
	'sites' : sites,
	'site_tree' : json.dumps(site_tree, cls=DjangoJSONEncoder),
	'footer' : datetime.datetime.now().year
	}
	# pprint.pprint(site_tree)
	return render(requests, template, context)


def stats(requests):
	url, level = requests.GET['url'], requests.GET['level']
	db_object = Wordpress.objects.filter(url = url)[0]
	header = ''
	template = None
	sub_pages = None
	word_count = None
	word_count_json = None
	word_bags = None
	sub_pages_json = None

	if level == 'page':
		template = 'page_stat.html'
		header = 'Post Statistics'
		word_count, word_bags = Analysis(db_object.content).word_counter()
		word_count = [[k.capitalize().encode('ascii', 'ignore'), word_count[k]] for k in word_count]
		word_count.sort(key=lambda x:x[1], reverse=True)
		word_count_json = json.dumps(word_count, cls=DjangoJSONEncoder) 
	elif level == 'site':
		template = 'site_stat.html'
		header = 'Site Statistics'
		sub_pages = Wordpress.objects.filter(parent=url)
		temp = [{'url' : page.url, 'title' : page.title, 'subtitle' : page.subtitle, 'published' : page.published} for page in sub_pages]
		temp = {'url' : db_object.url, 'title' : db_object.title, 'subtitle' : db_object.subtitle, 'published' : db_object.published, 'children' : temp}
		sub_pages_json = json.dumps(temp, cls=DjangoJSONEncoder)
	
	context = {
	'title' : 'Tufts Wordpress Analysis',
	'header' : header,
	'level' : level,
	'db_object' : db_object,
	'sub_pages' : sub_pages,
	'sub_pages_json' : sub_pages_json,
	'word_count' : word_count,
	'word_bags' : word_bags,
	'word_count_json' : word_count_json,
	'footer' : datetime.datetime.now().year
	}
	return render(requests, template, context)