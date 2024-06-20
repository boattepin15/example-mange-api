from django.contrib import admin
from core import models
admin.site.register(models.User)
admin.site.register(models.Mange)
admin.site.register(models.Episode)