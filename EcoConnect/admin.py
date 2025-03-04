from django.contrib import admin
from .models import WastePickup

@admin.register(WastePickup)
class WastePickupAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'pickup_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'address')
