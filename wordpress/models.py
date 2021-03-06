from django.db import models

# Create your models here.
class Wordpress(models.Model):
	# level can only be - root, site, page
	url = models.CharField(max_length=175, primary_key=True, unique=True)
	level = models.CharField(max_length=10)
	published = models.DateTimeField()
	parent = models.CharField(max_length=150, null=True)
	title = models.CharField(max_length=100)
	subtitle = models.CharField(max_length=100, blank=True)
	content = models.TextField(blank=True)
	
	def __repr__(self):
		return self.title

class SentimentWord(models.Model):
	word = models.CharField(max_length=75, primary_key=True, unique=True)
	score = models.IntegerField()

	def __repr__(self):
		return ' - '.join([self.word, str(self.score)])