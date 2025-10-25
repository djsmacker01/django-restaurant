from django.contrib import admin
from .models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for MenuItem model
    """

    # field to display list view
    list_display = [
        'name',
        'category',
        'price', 
        'is_available', 
        'created_at'

          ]

    # Fields you can click to view details   
    list_display_links = ['name']

    # Filters on the right sidebar
    list_filter = ['category', 'is_available', 'created_at']

    # Search functionality
    search_fields = ['name', 'description']

    # Fields that are read-only
    readonly_fields = ['created_at', 'updated_at']

    # How items are ordered
    ordering = ['category', 'name']

    # Number of items per page
    list_per_page = 20

# Register your models with admin class  here.
admin.site.register(MenuItem, MenuItemAdmin)
