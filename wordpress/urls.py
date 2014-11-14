from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import home

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'wordpress.views.home'),
    url(r'^stats/', 'wordpress.views.stats'),
)
