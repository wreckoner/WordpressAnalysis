''' Some common methods used by some of the apps. '''
import re, copy, stopwords, random, os


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
		self.word_list = re.compile(r'\b[\w\-\']+\b', re.IGNORECASE).findall(temp)
		''' Remove all stopwords from word list. '''
		for word in self.stopwords:
			self.word_list = filter(lambda x : x != word, self.word_list)
		

	def word_counter(self):
		words = self.word_list
		word_counts = {k:0 for k in words}
		for word in words:
			word_counts[word] += 1
		return word_counts