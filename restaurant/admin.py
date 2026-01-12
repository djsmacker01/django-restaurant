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
    list_display = [
        'name',
        'category',
        'price', 
        'is_available', 
        'has_image',
        'created_at',
        'updated_at'
    ]
    list_display_links = ['name']
    list_filter = ['category', 'is_available', 'created_at', 'updated_at']
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
        'email',
        'phone',
        'date',
        'time',
        'number_of_guests',
        'status_display',
        'created_at'
    ]
    list_display_links = ['name']
    list_filter = ['status', 'date', 'created_at', 'number_of_guests']
    search_fields = ['name', 'email', 'phone', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'  # Easy navigation by date
    ordering = ['-date', '-time']  # Show upcoming reservations first
    list_per_page = 25
    
    fieldsets = (
        ('Reservation Information', {
            'fields': ('user', 'name', 'email', 'phone')
        }),
        ('Date & Time', {
            'fields': ('date', 'time', 'number_of_guests')
        }),
        ('Details', {
            'fields': ('status', 'special_requests')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_display(self, obj):
        """Display status with color coding."""
        colors = {
            'pending': '#ffc107',  # Yellow
            'confirmed': '#28a745',  # Green
            'cancelled': '#dc3545',  # Red
            'completed': '#17a2b8',  # Blue
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
