from django.core.management.base import BaseCommand
from wordpress.models import Wordpress
from bs4 import BeautifulSoup
from collections import OrderedDict
from django.utils import timezone
import re, feedparser, requests, time, datetime

class Command(BaseCommand):
	help = 'Scrapes Tufts Wordpress Sites for data.'

	def handle(self, *args, **options):
		start = datetime.datetime.now()
		self.stdout.write('Scraping the Tufts Wordpress Sites\n')
		self.root = "http://sites.tufts.edu/"
		self.pages = 50			# No. of pages of root that will be crawled
		self.age = 6			# Sets the number of months from present beyond which posts are ignored.
		root_title, sites = self.scrape(self.root, 'root')
		prior_sites = [page.url for page in Wordpress.objects.filter(level='site')]
		print 'Prior number of sites %s' %len(prior_sites)
		for site in prior_sites:
			if site not in sites:
				sites.append(site)
		print 'Total number of sites %s' %len(sites)
		Wordpress.objects.all().delete()					# Delete all revious records
		self.save({'title' : root_title}, 'root')
		for site in sites:
			self.stdout.write('\nScraping %s' %site)
			try:
				site_obj = self.scrape(site, 'site')
				if site_obj:
					self.save(site_obj, 'site')
					for item in site_obj['entries']:
						try:
							self.save(item, 'page')
						except Exception as e:
							self.stdout.write("Error trying to save page: %s" %str(e))
			except Exception as e:
				self.stdout.write("Error trying to save site: %s" %str(e))
		stop = datetime.datetime.now()
		self.stdout.write("Total time taken to update : %s" %(stop-start))


	def scrape(self, url, level):
		if level == 'root':
			crawler = Crawl_Root(url)
			return crawler.crawl(self.pages)
		elif level == 'site':
			crawler = Crawl_Site(url, self.age)
			return crawler.mine()

	def save(self, object, level):
		if level == 'root':
			obj = Wordpress(url = self.root, level=level, published=timezone.now(), parent=None, title=object['title'], subtitle="", content="")
		elif level == 'site':
			obj = Wordpress(url = object['url'], level='site', published=timezone.now(), parent=self.root, title=object['title'], subtitle=object['subtitle'], content="")
		elif level == 'page':
			obj = Wordpress(url = object['url'], level='page', published=object['published'], parent=object['parent'], title=object['title'], subtitle="", content=object['content'])
		obj.save()



class  Crawl_Root():
	"""Crawler which crawls through the root site and returns all urls directed from it. Initialize with the url of the root site."""
	def __init__(self, url):
		self.url = url
		
	def crawl(self, pages):
	    links, title = [], ''
	    root = self.url
	    for page in xrange(1, pages+1):
	        html = requests.get(''.join([root, '?pg=%s'%page]))
	        soup = BeautifulSoup(html.content)
	        title = soup.title.text
	        for anchor in soup.find_all('a'):
	            if anchor.has_attr('href'):
	                if self.is_valid_html(anchor['href']):
	                    links.append(anchor['href'])
	    links = map(self.extract_link, links)
	    links = [link for link in links if link]
	    links = list(OrderedDict.fromkeys((self.prune_useless_links(links))))
	    links = [''.join([root, link, '/']) for link in links]
	    return title, links
	    
	def is_valid_html(self, url):
	    ''' Inspects the passed url and returns True if it's a valid url, else False. '''
	    flag = False
	    link_types = ['.jpg', '.jpeg', '.png', '.bmp']
	    urls = ['http://sites.tufts.edu/', 'http://sites.tufts.edu', '/']
	    if (url.startswith('http://sites.tufts.edu') or url.startswith('/')) and url not in urls:
	        flag = True
	    for link_type in link_types:
	        if url.endswith(link_type):
	            flag = False
	            break;
	    return flag

	def extract_link(self, url):
	    '''Extracts the ending portion from a tufts wordpress url'''
	    pat = re.compile(r'^(http://sites.tufts.edu)?(/)?([-_\w]*)')
	    tail = pat.findall(url)[0][-1]
	    if not tail == '': return tail
	    else: return None
	    
	def prune_useless_links(self, links):
	    ''' Removes useless urls from the list of urls. Update the list 'exclusion' as and when needed. '''
	    exclusions = ['faq', 'members', 'quick-start-guide', 'support', 'munchen', 'schweinehund', 'mph255ochoa']
	    return [link for link in links if link not in exclusions]


class Crawl_Site():
	"""Parses the feeds of each Tufts Wordpress site."""
	def __init__(self, url, age):
		self.url = url
		self.age = age
		
	def mine(self):
	    parsed = feedparser.parse(''.join([self.url, 'feed']))
	    site_data = {}
	    site_data['url'] = self.url
	    site_data['title'] = parsed.feed.title.encode('ascii', 'ignore')
	    site_data['subtitle'] = parsed.feed.description.encode('ascii', 'ignore')
	    site_data['entries'] = []
	    print '%s. %s' %(site_data['title'], site_data['subtitle'])
	    for entry in parsed.entries:
	        site_entry = {}
	        published = timezone.make_aware(datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed)), timezone.get_current_timezone())
	        if (timezone.now() - published).days > self.age * 30:
	        	print 'Page at %s is older than %s months. Discarding' %(entry.link, self.age)
	        else:
	        	try:
	        		print published, entry.link
		        	site_entry['url'] = entry.link
		        	site_entry['parent'] = self.url
		        	site_entry['published'] = published
			        site_entry['title'] = entry.title.encode('ascii', 'ignore')
			        site_entry['content'] = self.clean_text(entry.content[0]['value'])
			        site_data['word_count'] = None
			        site_data['top_words'] = None
			        site_data['entries'].append(site_entry)
	        	except Exception, e:
			    	print "Error parsing %s : %s" %(entry.link, str(e))
		if len(site_data['entries']) == 0:					# If all the posts are older than the age, returns false
			site_data = False
	    return site_data

	def clean_text(self, text):
		table = {'&#8211;' : '-', '&#8212;' : '-', '&#8216;' : "'", '&#8217;' : "'", '&#8220;' : '"', '&#8221;' : '"', '&nbsp;' : ' ', '&#8230;' : '...', "&amp;" : '&'}
		for pair in table:
			text = text.replace(pair, table[pair])
		text = re.sub(r'<.*?>|</.*?>', ' ', text)
		#return text.encode('ascii', 'ignore')
		return text