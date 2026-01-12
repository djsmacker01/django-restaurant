from django.db import models


class MenuItem(models.Model):
    """
    Model representing a menu item in the restaurant.
    
    """
    # Category choices
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),  # ← Added quotes
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('drink', 'Drink'),
    ]

    # fields
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
        ordering = ['category','name'],
        verbose_name = "Menu Item",
        verbose_name_plural = "Menu Items"
