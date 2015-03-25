from django.contrib import admin

# Register your models here.
from wordpress.models import Wordpress, SentimentWord


class WordpressAdmin(admin.ModelAdmin):
	list_display = ('url', 'level', 'parent')

class SentimentWordAdmin(admin.ModelAdmin):
	list_display = ('word', 'score')

admin.site.register(Wordpress, WordpressAdmin)
admin.site.register(SentimentWord, SentimentWordAdmin)