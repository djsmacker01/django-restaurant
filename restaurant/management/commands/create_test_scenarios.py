"""
Management command to create realistic test scenarios for comprehensive testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from restaurant.models import MenuItem, Order, OrderItem, Reservation
from decimal import Decimal
from datetime import time, timedelta
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Create realistic test scenarios for comprehensive testing'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('CREATING TEST SCENARIOS')
        self.stdout.write('=' * 60)
        
       
        if MenuItem.objects.count() < 5:
            self.stdout.write(
                self.style.WARNING(
                    '\nNot enough menu items. Run "python manage.py create_sample_data" first.'
                )
            )
            return
        
        self.create_complete_order_scenario()
        self.create_multiple_reservations_scenario()
        self.create_cart_with_multiple_items_scenario()
        self.create_mixed_status_orders_scenario()
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('TEST SCENARIOS CREATED!')
        self.stdout.write('=' * 60)

    def create_complete_order_scenario(self):
        """Create a complete order with multiple items."""
        self.stdout.write('\n[1/4] Creating Complete Order Scenario...')
        
        user, _ = User.objects.get_or_create(
            username='order_test_user',
            defaults={
                'email': 'order_test@example.com',
                'is_staff': False,
            }
        )
        user.set_password('testpass123')
        user.save()
        
      
        order = Order.objects.create(
            user=user,
            order_number='SCENARIO-001',
            status='completed',
            payment_status='paid',
            total_amount=Decimal('0.00'),
        )
        
       
        items = MenuItem.objects.filter(is_available=True)[:5]
        for item in items:
            OrderItem.objects.create(
                order=order,
                menu_item=item,
                quantity=random.randint(1, 2),
                price=item.price,
            )
        
        order.calculate_total()
        self.stdout.write(
            self.style.SUCCESS(
                f'  Created completed order: {order.order_number} '
                f'with {order.order_items.count()} items, Total: £{order.total_amount}'
            )
        )

    def create_multiple_reservations_scenario(self):
        """Create multiple reservations with different statuses."""
        self.stdout.write('\n[2/4] Creating Multiple Reservations Scenario...')
        
        user, _ = User.objects.get_or_create(
            username='reservation_test_user',
            defaults={
                'email': 'reservation_test@example.com',
                'is_staff': False,
            }
        )
        user.set_password('testpass123')
        user.save()
        
        scenarios = [
            {'days': 2, 'time': time(18, 0), 'guests': 2, 'status': 'pending'},
            {'days': 5, 'time': time(19, 30), 'guests': 4, 'status': 'confirmed'},
            {'days': 10, 'time': time(20, 0), 'guests': 6, 'status': 'confirmed'},
        ]
        
        for i, scenario in enumerate(scenarios):
            reservation = Reservation.objects.create(
                user=user,
                name=f'Test Reservation {i+1}',
                email=user.email,
                phone=f'0712345678{i}',
                date=timezone.now().date() + timedelta(days=scenario['days']),
                time=scenario['time'],
                number_of_guests=scenario['guests'],
                status=scenario['status'],
                special_requests=f'Special request {i+1}' if i > 0 else '',
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'  Created reservation: {reservation.name} '
                    f'({reservation.date}, {reservation.get_status_display()})'
                )
            )

    def create_cart_with_multiple_items_scenario(self):
        """Create a cart with multiple items for testing checkout."""
        self.stdout.write('\n[3/4] Creating Shopping Cart Scenario...')
        
        user, _ = User.objects.get_or_create(
            username='cart_test_user',
            defaults={
                'email': 'cart_test@example.com',
                'is_staff': False,
            }
        )
        user.set_password('testpass123')
        user.save()
        
     
        cart, created = Order.objects.get_or_create(
            user=user,
            status='pending',
            payment_status='pending',
            defaults={'order_number': 'CART-TEST-001'}
        )
        
        
        items = MenuItem.objects.filter(is_available=True)[:4]
        for item in items:
            OrderItem.objects.get_or_create(
                order=cart,
                menu_item=item,
                defaults={
                    'quantity': random.randint(1, 3),
                    'price': item.price,
                }
            )
        
        cart.calculate_total()
        self.stdout.write(
            self.style.SUCCESS(
                f'  Created cart with {cart.order_items.count()} items, '
                f'Total: £{cart.total_amount}'
            )
        )

    def create_mixed_status_orders_scenario(self):
        """Create orders with various statuses for testing."""
        self.stdout.write('\n[4/4] Creating Mixed Status Orders Scenario...')
        
        user, _ = User.objects.get_or_create(
            username='status_test_user',
            defaults={
                'email': 'status_test@example.com',
                'is_staff': False,
            }
        )
        user.set_password('testpass123')
        user.save()
        
        statuses = [
            ('processing', 'paid'),
            ('ready', 'paid'),
            ('completed', 'paid'),
            ('cancelled', 'refunded'),
        ]
        
        items = list(MenuItem.objects.filter(is_available=True)[:3])
        
        for i, (order_status, payment_status) in enumerate(statuses):
            order = Order.objects.create(
                user=user,
                order_number=f'STATUS-{i+1:03d}',
                status=order_status,
                payment_status=payment_status,
                total_amount=Decimal('0.00'),
            )
            
         
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=1,
                    price=item.price,
                )
            
            order.calculate_total()
            self.stdout.write(
                self.style.SUCCESS(
                    f'  Created order: {order.order_number} '
                    f'({order.get_status_display()}, {order.get_payment_status_display()})'
                )
            )













