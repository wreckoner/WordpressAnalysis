from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'home.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^$', include('home.urls')),
    url(r'^$', include('wordpress.urls')),
    url(r'^rssfeed/', 'rssfeed.views.api'),
    url(r'^admin/', include(admin.site.urls)),
)
