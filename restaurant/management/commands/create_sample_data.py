from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from restaurant.models import MenuItem, Order, OrderItem, Reservation
from decimal import Decimal
from datetime import date, time, timedelta
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Create comprehensive sample data for testing and demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--full',
            action='store_true',
            help='Create full dataset including users, orders, and reservations',
        )

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('CREATING SAMPLE DATA')
        self.stdout.write('=' * 60)
        
        # Create menu items
        self.create_menu_items()
        
        if options['full']:
            self.create_test_users()
            self.create_sample_orders()
            self.create_sample_reservations()
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write('FULL DATASET CREATED SUCCESSFULLY!')
            self.stdout.write('=' * 60)
        else:
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write('MENU ITEMS CREATED!')
            self.stdout.write('Use --full flag to create users, orders, and reservations')
            self.stdout.write('=' * 60)

    def create_menu_items(self):
        """Create comprehensive menu items."""
        self.stdout.write('\n[1/4] Creating Menu Items...')
        
        menu_items = [
            # Appetizers
            {
                'name': 'Caesar Salad',
                'description': 'Fresh romaine lettuce with parmesan cheese, croutons, and our signature Caesar dressing. A classic favorite.',
                'price': Decimal('8.99'),
                'category': 'appetizer',
                'is_available': True,
            },
            {
                'name': 'Bruschetta',
                'description': 'Toasted artisan bread topped with fresh tomatoes, basil, garlic, and mozzarella. Drizzled with extra virgin olive oil.',
                'price': Decimal('7.50'),
                'category': 'appetizer',
                'is_available': True,
            },
            {
                'name': 'Mozzarella Sticks',
                'description': 'Crispy golden mozzarella sticks served with marinara sauce. Perfect for sharing.',
                'price': Decimal('6.99'),
                'category': 'appetizer',
                'is_available': True,
            },
            {
                'name': 'Soup of the Day',
                'description': 'Chef\'s daily selection of homemade soup, served with fresh bread.',
                'price': Decimal('5.99'),
                'category': 'appetizer',
                'is_available': True,
            },
            {
                'name': 'Chicken Wings',
                'description': 'Spicy buffalo wings with blue cheese dip and celery sticks. Available in mild, medium, or hot.',
                'price': Decimal('9.99'),
                'category': 'appetizer',
                'is_available': True,
            },
            
            # Main Courses
            {
                'name': 'Grilled Salmon',
                'description': 'Fresh Atlantic salmon grilled to perfection, served with roasted vegetables and lemon butter sauce. A healthy and delicious choice.',
                'price': Decimal('24.99'),
                'category': 'main',
                'is_available': True,
            },
            {
                'name': 'Beef Tenderloin',
                'description': 'Premium cut of beef, cooked to your preference, served with mashed potatoes and seasonal vegetables. Our signature dish.',
                'price': Decimal('32.99'),
                'category': 'main',
                'is_available': True,
            },
            {
                'name': 'Margherita Pizza',
                'description': 'Classic Italian pizza with fresh mozzarella, tomato sauce, and basil. Simple and delicious.',
                'price': Decimal('14.99'),
                'category': 'main',
                'is_available': True,
            },
            {
                'name': 'Chicken Parmesan',
                'description': 'Breaded chicken breast with marinara sauce and melted mozzarella, served with pasta. A hearty Italian favorite.',
                'price': Decimal('18.99'),
                'category': 'main',
                'is_available': True,
            },
            {
                'name': 'Fish and Chips',
                'description': 'Beer-battered cod with crispy chips, mushy peas, and tartar sauce. A British classic.',
                'price': Decimal('16.99'),
                'category': 'main',
                'is_available': True,
            },
            {
                'name': 'Vegetarian Risotto',
                'description': 'Creamy arborio rice with seasonal vegetables, parmesan, and fresh herbs. A vegetarian delight.',
                'price': Decimal('15.99'),
                'category': 'main',
                'is_available': True,
            },
            {
                'name': 'BBQ Ribs',
                'description': 'Slow-cooked pork ribs with our house BBQ sauce, coleslaw, and fries. Fall-off-the-bone tender.',
                'price': Decimal('22.99'),
                'category': 'main',
                'is_available': True,
            },
            
            # Desserts
            {
                'name': 'Chocolate Lava Cake',
                'description': 'Warm chocolate cake with a molten center, served with vanilla ice cream. A decadent treat.',
                'price': Decimal('9.99'),
                'category': 'dessert',
                'is_available': True,
            },
            {
                'name': 'Tiramisu',
                'description': 'Classic Italian dessert with coffee-soaked ladyfingers and mascarpone cream. Light and elegant.',
                'price': Decimal('8.99'),
                'category': 'dessert',
                'is_available': True,
            },
            {
                'name': 'New York Cheesecake',
                'description': 'Rich and creamy cheesecake with a graham cracker crust. Topped with fresh berries.',
                'price': Decimal('8.50'),
                'category': 'dessert',
                'is_available': True,
            },
            {
                'name': 'Apple Pie',
                'description': 'Homemade apple pie with cinnamon and nutmeg, served warm with vanilla ice cream.',
                'price': Decimal('7.99'),
                'category': 'dessert',
                'is_available': True,
            },
            {
                'name': 'Ice Cream Sundae',
                'description': 'Three scoops of premium ice cream with chocolate sauce, whipped cream, and a cherry on top.',
                'price': Decimal('6.99'),
                'category': 'dessert',
                'is_available': True,
            },
            
            # Drinks
            {
                'name': 'Red Wine',
                'description': 'House selection of premium red wine. Ask your server for today\'s selection.',
                'price': Decimal('12.99'),
                'category': 'drink',
                'is_available': True,
            },
            {
                'name': 'White Wine',
                'description': 'House selection of premium white wine. Perfect pairing for seafood dishes.',
                'price': Decimal('12.99'),
                'category': 'drink',
                'is_available': True,
            },
            {
                'name': 'Fresh Orange Juice',
                'description': 'Freshly squeezed orange juice, served chilled. A refreshing start to your meal.',
                'price': Decimal('4.99'),
                'category': 'drink',
                'is_available': True,
            },
            {
                'name': 'Espresso',
                'description': 'Rich and bold Italian espresso. The perfect end to your meal.',
                'price': Decimal('3.50'),
                'category': 'drink',
                'is_available': True,
            },
            {
                'name': 'Cappuccino',
                'description': 'Espresso with steamed milk and foam. A classic Italian coffee.',
                'price': Decimal('4.50'),
                'category': 'drink',
                'is_available': True,
            },
            {
                'name': 'Coca Cola',
                'description': 'Classic soft drink, served ice cold.',
                'price': Decimal('2.99'),
                'category': 'drink',
                'is_available': True,
            },
            {
                'name': 'Craft Beer',
                'description': 'Selection of local craft beers. Ask your server for available options.',
                'price': Decimal('5.99'),
                'category': 'drink',
                'is_available': True,
            },
        ]
        
        created_count = 0
        for item_data in menu_items:
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  Created: {item.name} - £{item.price}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  Already exists: {item.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n  Total menu items: {MenuItem.objects.count()}'
            )
        )

    def create_test_users(self):
        """Create test users for demonstration."""
        self.stdout.write('\n[2/4] Creating Test Users...')
        
        users_data = [
            {
                'username': 'customer1',
                'email': 'customer1@example.com',
                'password': 'testpass123',
                'is_staff': False,
            },
            {
                'username': 'customer2',
                'email': 'customer2@example.com',
                'password': 'testpass123',
                'is_staff': False,
            },
            {
                'username': 'manager',
                'email': 'manager@restaurant.com',
                'password': 'testpass123',
                'is_staff': True,
            },
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'is_staff': user_data['is_staff'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  Created user: {user.username} '
                        f'({"Staff" if user.is_staff else "Customer"})'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  User already exists: {user.username}')
                )

    def create_sample_orders(self):
        """Create sample orders for testing."""
        self.stdout.write('\n[3/4] Creating Sample Orders...')
        
        # Get users and menu items
        customers = User.objects.filter(is_staff=False)[:2]
        menu_items = list(MenuItem.objects.filter(is_available=True))
        
        if not customers.exists() or not menu_items:
            self.stdout.write(
                self.style.WARNING('  Skipping orders: Need customers and menu items')
            )
            return
        
        order_scenarios = [
            {
                'status': 'completed',
                'payment_status': 'paid',
                'items_count': 3,
            },
            {
                'status': 'processing',
                'payment_status': 'paid',
                'items_count': 2,
            },
            {
                'status': 'ready',
                'payment_status': 'paid',
                'items_count': 4,
            },
        ]
        
        created_count = 0
        for i, customer in enumerate(customers):
            if i < len(order_scenarios):
                scenario = order_scenarios[i]
                
                # Create order
                order = Order.objects.create(
                    user=customer,
                    order_number=f'ORD-{1000 + i}',
                    status=scenario['status'],
                    payment_status=scenario['payment_status'],
                    total_amount=Decimal('0.00'),
                )
                
                # Add random items
                selected_items = random.sample(menu_items, min(scenario['items_count'], len(menu_items)))
                for item in selected_items:
                    quantity = random.randint(1, 3)
                    OrderItem.objects.create(
                        order=order,
                        menu_item=item,
                        quantity=quantity,
                        price=item.price,
                    )
                
                # Calculate total
                order.calculate_total()
                created_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  Created order: {order.order_number} '
                        f'({scenario["status"]}, £{order.total_amount})'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n  Total orders: {Order.objects.exclude(status="pending", payment_status="pending").count()}')
        )

    def create_sample_reservations(self):
        """Create sample reservations for testing."""
        self.stdout.write('\n[4/4] Creating Sample Reservations...')
        
        customers = User.objects.filter(is_staff=False)[:2]
        
        if not customers.exists():
            self.stdout.write(
                self.style.WARNING('  Skipping reservations: Need customers')
            )
            return
        
        reservation_scenarios = [
            {
                'name': 'John Smith',
                'phone': '07123456789',
                'date_offset': 3,
                'time': time(19, 0),
                'guests': 4,
                'status': 'confirmed',
                'special_requests': 'Window seat if possible',
            },
            {
                'name': 'Sarah Johnson',
                'phone': '07987654321',
                'date_offset': 7,
                'time': time(18, 30),
                'guests': 2,
                'status': 'pending',
                'special_requests': 'Anniversary dinner',
            },
            {
                'name': 'Michael Brown',
                'phone': '07555123456',
                'date_offset': 14,
                'time': time(20, 0),
                'guests': 6,
                'status': 'confirmed',
                'special_requests': 'Birthday celebration',
            },
        ]
        
        created_count = 0
        for i, customer in enumerate(customers):
            if i < len(reservation_scenarios):
                scenario = reservation_scenarios[i]
                reservation_date = timezone.now().date() + timedelta(days=scenario['date_offset'])
                
                reservation = Reservation.objects.create(
                    user=customer,
                    name=scenario['name'],
                    email=customer.email,
                    phone=scenario['phone'],
                    date=reservation_date,
                    time=scenario['time'],
                    number_of_guests=scenario['guests'],
                    special_requests=scenario['special_requests'],
                    status=scenario['status'],
                )
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  Created reservation: {reservation.name} '
                        f'({reservation_date}, {scenario["status"]})'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n  Total reservations: {Reservation.objects.count()}')
        )
