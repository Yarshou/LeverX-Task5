from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Homework)
admin.site.register(Solution)
admin.site.register(Mark)
admin.site.register(Commentary)
