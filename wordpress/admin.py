from django.contrib import admin

# Register your models here.
from wordpress.models import Wordpress


class WordpressAdmin(admin.ModelAdmin):
	list_display = ('url', 'level', 'parent')

admin.site.register(Wordpress, WordpressAdmin)