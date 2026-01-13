from django.contrib import admin
from django.utils.html import format_html
from .models import MenuItem, Order, OrderItem, Reservation


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem."""
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for MenuItem model
    Optimized for production content management
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
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'price')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload an image for this menu item. Recommended size: 800x600px or larger.'
        }),
        ('Availability', {
            'fields': ('is_available',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['category', 'name']
    list_per_page = 25
    list_editable = ['is_available', 'price']  # Quick edit from list view
    
    def has_image(self, obj):
        """Display checkmark if item has image."""
        return bool(obj.image)
    has_image.short_description = 'Has Image'
    has_image.boolean = True
    
    def image_preview(self, obj):
        """Display image preview in admin."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 8px;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">No image uploaded</span>')
    image_preview.short_description = 'Image Preview'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model."""
    list_display = [
        'order_number',
        'user',
        'status',
        'payment_status',
        'total_amount',
        'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    ordering = ['-created_at']
    list_per_page = 20


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Admin configuration for Reservation model."""
    list_display = [
        'name',
        'user',
        'date',
        'time',
        'number_of_guests',
        'status',
        'created_at'
    ]
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['name', 'user__username', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['date', 'time']
    list_per_page = 20

