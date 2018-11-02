from django.contrib import admin
from .models import Show, Horse, Rider, Classes

# Register your models here.

admin.site.register(Show)
admin.site.register(Horse)
admin.site.register(Rider)
admin.site.register(Classes)
