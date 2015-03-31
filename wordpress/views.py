from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from email.utils import parsedate_tz, mktime_tz
from models import Wordpress
from common.analyzer import Analysis
import json, datetime, pprint


def home(requests):
	'''Handler for the root/home page of the Wordpress Analysis Project.'''
	template = 'tuftsWPA.html'
	template = 'root_stat.html'
	db_object = Wordpress.objects.filter(level='root')[0]
	sites = Wordpress.objects.filter(level='site')
	site_tree = {'url' : db_object.url, 'title' : db_object.title, 'subtitle' : db_object.subtitle, 'published' : db_object.published, 'level' : db_object.level, 'children' : []}
	site_tree['children'] = [{'url' : site.url, 'title' : site.title, 'subtitle' : site.subtitle, 'published' : site.published, 'level' : site.level, 'children' : []} for site in sites]
	for site in site_tree['children']:
		temp = [{'url' : post.url, 'title' : post.title, 'subtitle' : post.subtitle, 'published' : post.published, 'level' : post.level} for post in Wordpress.objects.filter(parent=site['url'])]
		site['children'] = temp
	context = {
	'title' : 'Tufts WordPress Analysis',
	'header' : 'Tufts Wordpress Analysis (WPA) Project',
	'db_object' : db_object,
	'sites' : sites,
	'site_tree' : json.dumps(site_tree, cls=DjangoJSONEncoder),
	'footer' : datetime.datetime.now().year
	}
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


def api(requests):
	dump = {}
	try:
		start = timezone.make_aware(datetime.datetime.fromtimestamp(mktime_tz(parsedate_tz(requests.GET['from']))), timezone.get_current_timezone())
		stop = timezone.make_aware(datetime.datetime.fromtimestamp(mktime_tz(parsedate_tz(requests.GET['to']))), timezone.get_current_timezone())
		site = requests.GET['site']

		db_object = Wordpress.objects.filter(level='root')[0]
		site_tree = {'url' : db_object.url, 'title' : db_object.title, 'subtitle' : db_object.subtitle, 'published' : db_object.published, 'level' : db_object.level, 'children' : []}

		if site == 'all':
			pages = Wordpress.objects.filter(published__range = [start, stop]).filter(level='page')
		else:
			pages = Wordpress.objects.filter(published__range = [start, stop]).filter(parent=site)

		dump['page_count'] = len(pages)
		
		_sites = []
		for page in pages:
			if page.parent not in _sites:
				_sites.append(page.parent)


		sites = [Wordpress.objects.filter(url=site)[0] for site in _sites]
		site_tree['children'] = [{'url' : site.url, 'title' : site.title, 'subtitle' : site.subtitle, 'published' : site.published, 'level' : site.level, 'children' : []} for site in sites]
		dump['site_count'] = len(site_tree['children'])
		for site in site_tree['children']:
			temp = [{'url' : post.url, 'title' : post.title, 'subtitle' : post.subtitle, 'published' : post.published, 'level' : post.level} for post in pages if post.parent == site['url']]
			site['children'] = temp
		# pprint.pprint(site_tree)
		dump['site_tree'] = site_tree
		text_dump = ' '.join([page.content for page in pages])
		analysis_obj = Analysis(text_dump)
		word_count, word_bags = analysis_obj.word_counter()
		dump['word_count'] = word_count
		dump['word_bags'] = word_bags
		#print word_count
	except Exception as e:
		print str(e)
	return JsonResponse(dump)