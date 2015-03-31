''' Some common methods used by some of the apps. '''
import re, copy, stopwords, random, os
from collections import Counter
from operator import itemgetter
from wordpress.models import SentimentWord


class Analysis():
	""" Analysis Class. """
	def __init__(self, text):
		self.text = text
		
	def extract_words(self):
		''' Extract words appearing in the text. '''
		self.stopwords = stopwords.stop_words
		temp = self.text.lower()
		temp = re.sub(r'http.*? ', ' ', temp)
		temp = re.sub(r'\b\d+\b', '', temp)
		self.word_list = re.compile(r'\b[\w\-\']+\b', re.IGNORECASE|re.UNICODE).findall(temp)
		''' Remove all stopwords from word list. '''
		for word in self.stopwords:
			self.word_list = filter(lambda x : x != word, self.word_list)
		

	def word_counter(self):
		stopwords_pattern = re.compile(r'\b(' + r'|'.join(stopwords.stop_words) + r'|\d+|http.*?|www.*?)\b', re.I|re.U)
		pattern = re.compile(r'\b[\w\-\']+\b', re.I | re.U)

		text = stopwords_pattern.sub('', self.text)
		words = pattern.findall(text.lower())
		word_count = Counter(words).most_common(150)

		word_bags = [{'count' : count, 'words' : []} for count in sorted(({}.fromkeys(zip(*word_count)[1])).keys())[-50:]]
		for word in word_count:
			for bag in word_bags:
				if bag['count'] == word[1]:
					bag['words'].append(word[0])

		word_count = [{'text' : item[0], 'count' : item[1]} for item in word_count]
		return word_count, word_bags

	def sentiment_analyzer(self):
		sentiment_words = SentimentWord.objects.all()