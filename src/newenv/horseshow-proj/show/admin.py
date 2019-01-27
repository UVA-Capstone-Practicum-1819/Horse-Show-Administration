from django.contrib import admin
from .models import *

#Models are registered here.

admin.site.register(Show)
admin.site.register(Horse)
admin.site.register(Rider)
admin.site.register(Class)
admin.site.register(Division)
admin.site.register(HorseRiderCombo)
admin.site.register(ClassParticipation)
