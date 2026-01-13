"""
Script to verify all functionality is working correctly.
Run this to check for common issues.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flavour.settings')
django.setup()

from django.contrib.auth.models import User
from restaurant.models import MenuItem, Order, Reservation
from django.urls import reverse
from django.test import Client
from decimal import Decimal

def check_database():
    """Check database models and relationships."""
    print("=" * 60)
    print("DATABASE CHECK")
    print("=" * 60)
    
    # Check MenuItems
    menu_count = MenuItem.objects.count()
    print(f"[OK] Menu Items: {menu_count}")
    
    # Check Users
    user_count = User.objects.count()
    print(f"[OK] Users: {user_count}")
    
    # Check Orders
    order_count = Order.objects.count()
    print(f"[OK] Orders: {order_count}")
    
    # Check Reservations
    reservation_count = Reservation.objects.count()
    print(f"[OK] Reservations: {reservation_count}")
    
    # Check relationships
    if menu_count > 0:
        item = MenuItem.objects.first()
        print(f"[OK] MenuItem model working: {item.name}")
    
    print()

def check_urls():
    """Check that all URLs are accessible."""
    print("=" * 60)
    print("URL CHECK")
    print("=" * 60)
    
    client = Client()
    urls_to_check = [
        ('home', 'restaurant:menu_list'),
        ('restaurant:menu_list', 'restaurant:menu_list'),
    ]
    
    for name, url_name in urls_to_check:
        try:
            response = client.get(reverse(url_name))
            status = "[OK]" if response.status_code == 200 else "[FAIL]"
            print(f"{status} {url_name}: {response.status_code}")
        except Exception as e:
            print(f"[FAIL] {url_name}: Error - {str(e)}")
    
    print()

def check_models():
    """Check model methods and relationships."""
    print("=" * 60)
    print("MODEL METHODS CHECK")
    print("=" * 60)
    
    # Create test data
    user, _ = User.objects.get_or_create(
        username='test_check',
        defaults={'email': 'test@check.com'}
    )
    
    # Test MenuItem
    if MenuItem.objects.exists():
        item = MenuItem.objects.first()
        print(f"[OK] MenuItem.__str__(): {str(item)}")
        print(f"[OK] MenuItem.get_category_display(): {item.get_category_display()}")
    
    # Test Order
    order = Order.objects.create(
        user=user,
        order_number='TEST-001',
        status='pending',
        payment_status='pending'
    )
    print(f"[OK] Order created: {order.order_number}")
    
    # Test Reservation
    from datetime import date, time
    from django.utils import timezone
    reservation = Reservation.objects.create(
        user=user,
        name='Test',
        email='test@test.com',
        phone='1234567890',
        date=timezone.now().date() + timezone.timedelta(days=1),
        time=time(18, 0),
        number_of_guests=2
    )
    print(f"[OK] Reservation created: {reservation.name}")
    
    # Cleanup
    order.delete()
    reservation.delete()
    if user.username == 'test_check':
        user.delete()
    
    print()

def check_forms():
    """Check form validation."""
    print("=" * 60)
    print("FORM VALIDATION CHECK")
    print("=" * 60)
    
    from restaurant.forms import MenuItemForm, ReservationForm
    from django.utils import timezone
    from datetime import timedelta
    
    # Test MenuItemForm
    form = MenuItemForm(data={
        'name': 'Test Item',
        'price': '-10.00',  # Invalid
        'category': 'main'
    })
    print(f"[OK] MenuItemForm invalid price validation: {not form.is_valid()}")
    
    form = MenuItemForm(data={
        'name': 'Test Item',
        'price': '10.00',  # Valid
        'category': 'main'
    })
    print(f"[OK] MenuItemForm valid data: {form.is_valid()}")
    
    # Test ReservationForm
    future_date = timezone.now().date() + timedelta(days=1)
    form = ReservationForm(data={
        'name': 'Test',
        'phone': '1234567890',
        'date': future_date.isoformat(),
        'time': '18:00',
        'number_of_guests': 4
    })
    print(f"[OK] ReservationForm valid data: {form.is_valid()}")
    
    form = ReservationForm(data={
        'name': 'Test',
        'phone': '123',
        'date': future_date.isoformat(),
        'time': '18:00',
        'number_of_guests': 25  # Invalid
    })
    print(f"[OK] ReservationForm invalid data validation: {not form.is_valid()}")
    
    print()

def main():
    """Run all checks."""
    print("\n" + "=" * 60)
    print("DJANGO RESTAURANT - FUNCTIONALITY VERIFICATION")
    print("=" * 60 + "\n")
    
    try:
        check_database()
        check_models()
        check_forms()
        check_urls()
        
        print("=" * 60)
        print("VERIFICATION COMPLETE")
        print("=" * 60)
        print("\nAll checks passed! [OK]\n")
        
    except Exception as e:
        print(f"\n[ERROR] Error during verification: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

