from .base import *

try:
	from .local import *
	live = Frue
except:
	live = True

if live:
	from .production import *