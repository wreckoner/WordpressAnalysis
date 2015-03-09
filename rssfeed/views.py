from django.shortcuts import render
from django.http import JsonResponse
from common.analyzer import Analysis
import feedparser, re

# Create your views here.

def api(requests):
	dispatch = {}
	try:
		url = requests.GET['url']
		parsed = feedparser.parse(url)
		dispatch['title'] = parsed.feed.title
		dispatch['description'] = parsed.feed.description
		words = ''
		for entry in parsed.entries:
			words += entry.content[0]['value'] + '. '
		words = re.sub(r'<.*?>|</.*?>', ' ', words)
		table = {'&#8211;' : '-', '&#8212;' : '-', '&#8216;' : "'", '&#8217;' : "'", '&#8220;' : '"', '&#8221;' : '"', '&nbsp;' : ' ', '&#8230;' : '...', "&amp;" : '&'}
		for pair in table:
			words = words.replace(pair, table[pair])
		word_count, word_bags = Analysis(words).word_counter()
		dispatch['word_counts'] = word_count
		dispatch['word_bags'] = word_bags
		dispatch['status'] = True
		dispatch['message'] = 'success'
	except Exception as e:
		dispatch['status'] = False
		dispatch['message'] = str(e)
	return JsonResponse(dispatch)