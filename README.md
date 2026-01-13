# Django Restaurant 🍽️

A full-stack restaurant management web application I built with Django. This project lets customers browse menus, place orders, make reservations, and handle payments through Stripe. It's been a great learning experience building something that actually works end-to-end!

## What This Project Does

This is a complete restaurant platform where:

**For Customers:**
- Browse and search through menu items organized by category
- Add items to a shopping cart and manage quantities
- Checkout securely using Stripe payment processing
- View order history and track order status
- Make table reservations with date/time validation
- Manage their reservations (view, update, cancel)

**For Staff:**
- Manage menu items (add, edit, delete) through a staff-only interface
- View and manage customer orders
- View and manage reservations
- Access everything through the Django admin panel

**Why Login is Required:**
I made authentication required for orders and reservations because it ensures we can track order history, contact customers for delivery, process payments securely, and manage reservations properly. It's a real-world requirement that makes sense for a restaurant platform.

## Features I'm Proud Of

### Menu System
- Clean, organized menu browsing with category filters
- Search functionality to find items quickly
- Detailed item pages with images and descriptions
- Staff can easily add/edit menu items with image uploads

### Shopping Cart & Checkout
- Full shopping cart functionality (add, update quantities, remove items)
- Secure Stripe integration for payments
- Order tracking with status updates
- Order history so customers can see past purchases
- PDF invoice generation for completed orders

### Reservations
- Easy reservation booking system
- Smart validation (can't book in the past, must be during business hours)
- Guest count validation (1-20 people)
- Customers can view, update, or cancel their reservations

### Authentication & Security
- User registration and login using django-allauth
- Staff-only access to admin functions
- Environment variables for all sensitive data
- CSRF protection and secure password handling

## Tech Stack

I used:
- **Backend**: Django 5.2.7 with Python 3.13
- **Database**: SQLite for development (easy to switch to PostgreSQL for production)
- **Authentication**: django-allauth (handles all the auth complexity)
- **Payments**: Stripe (industry standard, secure, well-documented)
- **Frontend**: Bootstrap 5.3 for responsive design
- **Image Handling**: Pillow for menu item images
- **PDF Generation**: ReportLab for invoice creation

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (comes with Python)
- Git (if you're cloning this)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django-restaurant
   ```

2. **Set up a virtual environment** (trust me, you want this)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
   STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
   ```
   
   **Important**: Never commit your `.env` file! It's already in `.gitignore`.

5. **Set up the database**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (so you can access the admin panel)
   ```bash
   python manage.py createsuperuser
   ```

7. **Load some sample data** (optional, but helpful for testing)
   ```bash
   python manage.py create_sample_data --full
   ```
   
   This creates menu items, test users, sample orders, and reservations. Super handy for seeing how everything works!

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Open your browser**
   - Home: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/
   - Menu: http://127.0.0.1:8000/restaurant/menu/

## Stripe Setup (For Payments)

To get payments working:

1. Sign up for a free Stripe account at https://stripe.com
2. Get your test API keys from the Stripe Dashboard (make sure you're in test mode!)
3. Add them to your `.env` file:
   ```env
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   ```
4. Restart your Django server
5. Test with Stripe's test card: `4242 4242 4242 4242`

I've included detailed guides in the repo:
- `QUICK_STRIPE_SETUP.md` - Fast setup guide
- `STRIPE_SETUP_GUIDE.md` - More detailed instructions
- `DEBUG_CHECKOUT.md` - Troubleshooting tips

## Testing

I wrote a comprehensive test suite covering models, forms, views, and custom logic. Run it with:

```bash
python manage.py test
```

The tests cover:
- Model creation and relationships
- Form validation
- View authorization (who can access what)
- Custom Python logic (loops, conditionals, calculations)
- Cart operations
- Order processing

All 31+ tests should pass! 🎉

## Project Structure

```
django-restaurant/
├── flavour/              # Main Django project
│   ├── settings.py      # Configuration
│   ├── urls.py          # Root URL routing
│   └── views.py         # Home page view
├── restaurant/          # Main app (where the magic happens)
│   ├── models.py        # Database models
│   ├── views.py         # All the view functions
│   ├── forms.py         # Form classes with validation
│   ├── urls.py          # App URL routing
│   ├── admin.py         # Admin configuration
│   ├── tests.py         # Test suite
│   └── templates/       # HTML templates
├── templates/           # Project-level templates
│   ├── base.html        # Base template with navigation
│   └── home.html        # Home page
├── media/               # User-uploaded files (menu images)
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Key Features Explained

### Custom Python Logic

I implemented several custom functions that demonstrate Python proficiency:

**Order Total Calculation:**
```python
def calculate_total(self):
    total = Decimal('0.00')
    for item in self.order_items.all():
        total += item.subtotal
    return total
```

**Menu Filtering by Category:**
```python
categories = {}
for item in menu_items:
    if item.category not in categories:
        categories[item.category] = []
    categories[item.category].append(item)
```

**Reservation Validation:**
```python
if date < today:
    raise ValidationError("Date cannot be in the past.")
if time < opening_time or time > closing_time:
    raise ValidationError("Outside business hours.")
```

### Database Relationships

The models are connected with proper relationships:
- `User` → `Order` (one user can have many orders)
- `Order` → `OrderItem` (one order can have many items)
- `OrderItem` → `MenuItem` (each item references a menu item)
- `User` → `Reservation` (one user can have many reservations)

This ensures data integrity and makes querying efficient.

## Deployment

For production deployment, I've set up:

- Environment-based configuration (dev vs production)
- Security settings (HTTPS, secure cookies, etc.)
- Static file handling
- Database configuration options

The project is ready to deploy on platforms like:
- Heroku
- Railway
- PythonAnywhere
- Any platform that supports Django

Just make sure to:
1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up environment variables on your hosting platform
5. Run `python manage.py collectstatic`

## What I Learned

Building this project taught me:
- How to structure a full-stack Django application
- Implementing authentication and authorization properly
- Integrating third-party APIs (Stripe)
- Writing comprehensive tests
- Building user-friendly forms with validation
- Managing file uploads (menu images)
- Creating PDFs programmatically (invoices)
- Following Django best practices

## Future Improvements

If I were to continue working on this, I'd add:
- Email notifications for orders and reservations
- Real-time order status updates
- Customer reviews and ratings
- Delivery tracking
- Admin dashboard with analytics
- Mobile app API endpoints

## Contributing

This is a personal project, but if you find bugs or have suggestions, feel free to open an issue or submit a pull request!

## License

This project was created for educational purposes.

## Contact

Questions? Feel free to reach out or open an issue on GitHub.

---

**Note**: This application is designed for educational purposes. For production use, you'd want to add additional security measures, error handling, and performance optimizations. But it's a solid foundation that demonstrates full-stack development skills!
