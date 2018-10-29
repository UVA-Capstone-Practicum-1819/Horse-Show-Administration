from django.contrib import admin

# Register your models here.

from .models import Show, Horse, Rider, Combo

admin.site.register(Show)
admin.site.register(Horse)
admin.site.register(Rider)
admin.site.register(Combo)
