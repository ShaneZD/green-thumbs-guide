from django.contrib import admin
from .models import Plant, Garden, GardenPlant

class GardenPlantAdmin(admin.ModelAdmin):
    list_display = ('plant', 'garden', 'planted_date', 'last_watered', 'last_fertilized', 'last_pruned')
    fields = ('garden', 'plant', 'planted_date', 'last_watered', 'last_fertilized', 'last_pruned', 'notes')

admin.site.register(Plant)
admin.site.register(Garden)
admin.site.register(GardenPlant, GardenPlantAdmin)