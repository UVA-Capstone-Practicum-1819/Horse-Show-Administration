from django.contrib import admin
from .models import Show, Horse, Rider, Classes, Division

# Register your models here.

admin.site.register(Show)
admin.site.register(Horse)
admin.site.register(Rider)
admin.site.register(Classes)
admin.site.register(Division)
