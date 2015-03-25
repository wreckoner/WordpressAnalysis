from django.core.management.base import BaseCommand
from wordpress.models import SentimentWord
import requests, re


class Command(BaseCommand):
	''' Stores sentiment words to the table SentimentWord.'''

	def handle(self, *args, **options):
		url = "https://raw.githubusercontent.com/abromberg/sentiment_analysis/master/AFINN/AFINN-111.txt"
		response = requests.get(url)
		#print response.text
		for line in response.text.split('\n'):
			word, score = line.strip().split('\t')
			try:
				obj = SentimentWord(word=word, score=int(score))
				obj.save()
				self.stdout.write(u''.join(['Saved : ', word, score]))
			except Exception, e:
				self.stdout.write(str(e))
				