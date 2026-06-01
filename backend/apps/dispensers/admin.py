from django.contrib import admin

# Register your models here.

from .models import Dispenser, DispenserUsage

@admin.register(Dispenser)
class DispenserAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow_volume', 'status',)
    search_fields = ('status',)
    

@admin.register(DispenserUsage)
class DispenserUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'dispenser', 'opened_at', 'closed_at', 'flow_volume')
    search_fields = ('dispenser',)