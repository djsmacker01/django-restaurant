from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class MenuItem(models.Model):
    """
    Model representing a menu item in the restaurant.
    
    """
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),  # ← Added quotes
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('drink', 'Drink'),
    ]

    name = models.CharField(
        max_length=200,
        help_text = "Enter the name of the menu item"
        
        )
    description = models.TextField(
        blank=True,
        help_text = "Enter the description of the menu item"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text = "Price in £"
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='main',
        help_text = "Select the category of the menu item"
    )

    image = models.ImageField(
        upload_to='menu_images/',
        blank=True,
        null=True,
        help_text = "Upload an image of the menu item"
    )

    is_available = models.BooleanField(
        default=True,
        help_text = "Is the menu item available?"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text = "Date and time the menu item was created"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text = "Date and time the menu item was last updated"
    )

    def __str__(self):
        return self.name

    class Meta:
        """" 
        Metadata for the menu item model.
        """    
        ordering = ['category', 'name']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"


class Order(models.Model):
    """
    Model representing a customer order.
    Users need to register/login to place orders for food delivery or pickup.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="User who placed the order"
    )
    order_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique order number"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the order"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        help_text="Payment status of the order"
    )
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Stripe payment intent ID"
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Total amount of the order"
    )
    delivery_address = models.TextField(
        blank=True,
        help_text="Delivery address if applicable"
    )
    special_instructions = models.TextField(
        blank=True,
        help_text="Special instructions for the order"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time the order was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time the order was last updated"
    )
    
    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"
    
    def calculate_total(self):
        """Calculate total amount from order items."""
        total = Decimal('0.00')
        for item in self.order_items.all():
            total += item.subtotal
        self.total_amount = total
        self.save()
        return total
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    """
    Model representing an item in an order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        help_text="Order this item belongs to"
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        help_text="Menu item ordered"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Quantity of the menu item"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price at the time of order"
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Subtotal for this item (price * quantity)"
    )
    
    def save(self, *args, **kwargs):
        """Calculate subtotal before saving."""
        if not self.price:
            self.price = self.menu_item.price
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)
        self.order.calculate_total()
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} in Order {self.order.order_number}"
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"


class Reservation(models.Model):
    """
    Model representing a table reservation.
    Users need to register/login to make reservations to ensure we can contact them.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations',
        help_text="User who made the reservation"
    )
    name = models.CharField(
        max_length=200,
        help_text="Name for the reservation"
    )
    email = models.EmailField(
        help_text="Email address for the reservation"
    )
    phone = models.CharField(
        max_length=20,
        help_text="Phone number for the reservation"
    )
    date = models.DateField(
        help_text="Date of the reservation"
    )
    time = models.TimeField(
        help_text="Time of the reservation"
    )
    number_of_guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Number of guests"
    )
    special_requests = models.TextField(
        blank=True,
        help_text="Special requests or dietary requirements"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Status of the reservation"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time the reservation was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time the reservation was last updated"
    )
    
    def __str__(self):
        return f"Reservation for {self.name} on {self.date} at {self.time}"
    
    class Meta:
        ordering = ['date', 'time']
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"