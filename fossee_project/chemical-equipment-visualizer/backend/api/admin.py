"""
Django admin configuration for Dataset model.
"""

from django.contrib import admin
from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    """
    Admin interface for Dataset model.
    """
    list_display = ['id', 'name', 'user', 'total_equipment', 'uploaded_at']
    list_filter = ['uploaded_at', 'user']
    search_fields = ['name', 'user__username']
    readonly_fields = ['uploaded_at', 'data_json', 'equipment_distribution']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'file', 'uploaded_at')
        }),
        ('Statistics', {
            'fields': ('total_equipment', 'avg_flowrate', 'avg_pressure', 
                      'avg_temperature', 'equipment_distribution')
        }),
        ('Data', {
            'fields': ('data_json',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Disable manual addition through admin (use API instead)."""
        return False