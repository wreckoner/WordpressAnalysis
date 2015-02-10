''' Some common methods used by some of the apps. '''
import re, copy, stopwords, random, os
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
		self.word_list = re.compile(r'\b[\w\-\']+\b', re.IGNORECASE).findall(temp)
		''' Remove all stopwords from word list. '''
		for word in self.stopwords:
			self.word_list = filter(lambda x : x != word, self.word_list)
		

	def word_counter(self):
		words = self.word_list
		word_counts = {k:0 for k in words}
		word_bags = []
		for word in words:
			word_counts[word] += 1

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
		# for i in word_counts.values():
		# 	if i not in word_bags.keys():
		# 		word_bags[i] = []
		# for word in word_counts:
		# 	word_bags[word_counts[word]].append(word.capitalize())
		return word_counts, word_bags
