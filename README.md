Tufts Wordpress Analysis

AT Fellows project. This is a Django Web Application that scrapes the rss feeds of the WordPress sites under sites.tufts.edu, and saves them to a database. A user can then view trends in the data and other visualizations from this website. There's a version currently hosted on http://tufts.herokuapp.com/wordpress

Link to Tufts University Wordpress sites : http://sites.tufts.edu/

Apps :
1. wordpress - A WordPress analysis tool. Includes a management command to scrape WordPress sites under sites.tufts.edu and store the data in a database. Users can then analyze the data to see statistics such as site activity, wordcloud, etc from a browser. Note: The scraper aactually aggregates information from the rss feed of the blogs and not the html. Also it stores page data only from posts published within the last 6 months. You can change this setting in the code.

2. rssfeed - A rss feed parsing API. You need to provide the url to an rssfeed and the backend will parse it and return a json containing the title of the feed, and word counts of the text in the feed. You can alter the code to get back more information. Usage example (on local machine): http://localhost:8000/?url=http://sites.tufts.edu/reinventingpeace/feed

Deploying on local computer.
You can deploy this application on your computer either directly or through a python virtual environment. The later one is recommended.