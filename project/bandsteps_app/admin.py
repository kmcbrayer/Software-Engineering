from django.contrib import admin
from bandsteps_app.models import *

class DrillAdmin(admin.ModelAdmin):
	list_display = ['name','location_1', 'location_2','instructor']

admin.site.register(Drill, DrillAdmin)

class SetAdmin(admin.ModelAdmin):
	list_display = ['number','current','drill']

admin.site.register(Set, SetAdmin)

class LocationsAdmin(admin.ModelAdmin):
	list_display = ['set','s_id','rel_x','rel_y']

admin.site.register(StudentLoc, LocationsAdmin)