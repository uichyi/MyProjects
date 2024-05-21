from django.contrib import admin

from imageboard.models import *

admin.site.register(Board)
admin.site.register(Thread)
admin.site.register(Post)