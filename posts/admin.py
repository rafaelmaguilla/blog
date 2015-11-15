from django.contrib import admin
from posts.models import *

# Register your models here.
admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Reader)
admin.site.register(Comment)
