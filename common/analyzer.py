''' Some common methods used by some of the apps. '''
import re, copy, stopwords, random, os
from collections import Counter
from operator import itemgetter


class Analysis():
	""" Analysis Class. """
	def __init__(self, text):
		self.stopwords = stopwords.stop_words
		self.text = text
		self.extract_words()
		
	def extract_words(self):
		''' Extract words appearing in the text. '''
		temp = self.text.lower()
		temp = re.sub(r'http.*? ', ' ', temp)
		temp = re.sub(r'\b\d+\b', '', temp)
		self.word_list = re.compile(r'\b[\w\-\']+\b', re.IGNORECASE|re.UNICODE).findall(temp)
		''' Remove all stopwords from word list. '''
		for word in self.stopwords:
			self.word_list = filter(lambda x : x != word, self.word_list)
		

	def word_counter(self):
		words = self.word_list
		word_counts = dict(Counter(words).most_common(50))
		word_bags = []
		for word in word_counts:
			flag = False
			for bag in word_bags:
				if bag['count'] == word_counts[word]:
					bag['words'].append(word)
					flag = True
					break
			if not flag:
				word_bags.append({'count' : word_counts[word], 'words' : [word]})
		word_bags.sort(key=itemgetter('count'))
		if len(word_bags) > 50:
			word_bags = word_bags[-50:]
		word_counts = [{'text' : item, 'count' : word_counts[item]} for item in word_counts]
		word_counts.sort(key=lambda x:x['count'], reverse=True)
		return word_counts, word_bags
