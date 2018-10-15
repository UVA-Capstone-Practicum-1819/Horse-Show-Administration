from django.contrib import admin

# Register your models here.

from .models import Show, Horse

admin.site.register(Show)
admin.site.register(Horse)
