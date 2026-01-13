from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from .models import MenuItem, Order, Reservation


class MenuItemForm(forms.ModelForm):
    """
    Form for creating and editing menu items.
    Includes validation for price and availability.
    """
    
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'image', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter menu item name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_price(self):
        """Validate that price is positive."""
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price
    
    def clean_name(self):
        """Validate that name is not empty."""
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) == 0:
            raise ValidationError("Name cannot be empty.")
        return name.strip()


class ReservationForm(forms.ModelForm):
    """
    Form for creating table reservations.
    Includes validation for date, time, and number of guests.
    """
    
    class Meta:
        model = Reservation
        fields = ['name', 'phone', 'date', 'time', 'number_of_guests', 'special_requests']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': timezone.now().date().isoformat()
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'number_of_guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '20'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requests or dietary requirements'
            }),
        }
    
    def clean_date(self):
        """Validate that reservation date is in the future."""
        date = self.cleaned_data.get('date')
        if date:
            today = timezone.now().date()
            if date < today:
                raise ValidationError("Reservation date cannot be in the past.")
            # Check if date is too far in the future (e.g., 3 months)
            max_date = today + timedelta(days=90)
            if date > max_date:
                raise ValidationError("Reservations can only be made up to 3 months in advance.")
        return date
    
    def clean_time(self):
        """Validate that reservation time is during business hours."""
        time = self.cleaned_data.get('time')
        if time:
            # Business hours: 11:00 AM to 10:00 PM
            opening_time = datetime.strptime('11:00', '%H:%M').time()
            closing_time = datetime.strptime('22:00', '%H:%M').time()
            if time < opening_time or time > closing_time:
                raise ValidationError("Reservations can only be made between 11:00 AM and 10:00 PM.")
        return time
    
    def clean_number_of_guests(self):
        """Validate number of guests."""
        guests = self.cleaned_data.get('number_of_guests')
        if guests and (guests < 1 or guests > 20):
            raise ValidationError("Number of guests must be between 1 and 20.")
        return guests
    
    def clean_phone(self):
        """Basic phone number validation."""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove common separators
            phone_clean = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
            if not phone_clean.isdigit() or len(phone_clean) < 10:
                raise ValidationError("Please enter a valid phone number.")
        return phone


class OrderItemForm(forms.Form):
    """
    Form for adding items to cart/order.
    """
    menu_item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '10',
            'value': '1'
        })
    )
    
    def clean_quantity(self):
        """Validate quantity."""
        quantity = self.cleaned_data.get('quantity')
        if quantity and (quantity < 1 or quantity > 10):
            raise ValidationError("Quantity must be between 1 and 10.")
        return quantity











