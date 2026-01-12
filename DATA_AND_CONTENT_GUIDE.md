# Data and Content Guide

This document provides comprehensive information about sample data, image handling, and test scenarios for the Django Restaurant application.

## Table of Contents

1. [Sample Data Creation](#sample-data-creation)
2. [Image Handling](#image-handling)
3. [Test Scenarios](#test-scenarios)
4. [Test Users](#test-users)
5. [Real Data Scenarios](#real-data-scenarios)

---

## Sample Data Creation

### Quick Start

To create sample menu items only:
```bash
python manage.py create_sample_data
```

To create a full dataset (menu items, users, orders, reservations):
```bash
python manage.py create_sample_data --full
```

### Menu Items

The sample data command creates **25 menu items** across 4 categories:

#### Appetizers (5 items)
- Caesar Salad - £8.99
- Bruschetta - £7.50
- Mozzarella Sticks - £6.99
- Soup of the Day - £5.99
- Chicken Wings - £9.99

#### Main Courses (7 items)
- Grilled Salmon - £24.99
- Beef Tenderloin - £32.99
- Margherita Pizza - £14.99
- Chicken Parmesan - £18.99
- Fish and Chips - £16.99
- Vegetarian Risotto - £15.99
- BBQ Ribs - £22.99

#### Desserts (5 items)
- Chocolate Lava Cake - £9.99
- Tiramisu - £8.99
- New York Cheesecake - £8.50
- Apple Pie - £7.99
- Ice Cream Sundae - £6.99

#### Drinks (7 items)
- Red Wine - £12.99
- White Wine - £12.99
- Fresh Orange Juice - £4.99
- Espresso - £3.50
- Cappuccino - £4.50
- Coca Cola - £2.99
- Craft Beer - £5.99

### Features

- **Idempotent**: Running the command multiple times won't create duplicates
- **Comprehensive**: Covers all menu categories with realistic items
- **Descriptive**: Each item includes detailed descriptions
- **Priced**: Realistic pricing for a restaurant setting

---

## Image Handling

### Placeholder System

The application includes a robust image placeholder system that handles missing images gracefully:

#### Visual Placeholders

When a menu item doesn't have an image uploaded, the system displays:
- **Gradient background**: Purple gradient (from `#667eea` to `#764ba2`)
- **Icon**: Font Awesome utensils icon (`fa-utensils`)
- **Consistent sizing**: Maintains aspect ratio and dimensions

#### Implementation Locations

Image placeholders are implemented in:

1. **Menu List** (`menu_list.html`)
   - Card images: 240px height
   - Gradient background with icon

2. **Menu Detail** (`menu_detail.html`)
   - Large image: 500px height
   - Full-width display

3. **Home Page Featured Items** (`home.html`)
   - Featured cards: 280px height
   - Consistent with menu list styling

4. **Shopping Cart** (`cart.html`)
   - Thumbnail images: 60x60px
   - Small icon in gradient circle

5. **Order Detail** (`order_detail.html`)
   - Order item images: 50x50px
   - Compact display for order history

6. **Checkout Page** (`checkout.html`)
   - Order summary images: 60x60px
   - Consistent with cart styling

### Adding Real Images

To add images to menu items:

1. **Via Admin Interface**:
   - Navigate to `/admin/restaurant/menuitem/`
   - Edit a menu item
   - Upload an image (supports JPG, PNG, GIF)
   - Images are stored in `media/menu_images/`

2. **Via Staff Form**:
   - Log in as staff user
   - Navigate to Menu → Create/Edit
   - Upload image through the form

3. **Image Requirements**:
   - Format: JPG, PNG, GIF
   - Recommended size: 800x600px or larger
   - Storage: `media/menu_images/` directory
   - Django handles resizing and optimization

### Image Storage

- **Development**: Images stored in `media/menu_images/`
- **Production**: Configure `MEDIA_ROOT` and `MEDIA_URL` in settings
- **Static Files**: Run `python manage.py collectstatic` for production

---

## Test Scenarios

### Creating Test Scenarios

Run the test scenarios command:
```bash
python manage.py create_test_scenarios
```

This creates comprehensive test data for:

### 1. Complete Order Scenario
- **User**: `order_test_user`
- **Order**: `SCENARIO-001`
- **Status**: Completed
- **Items**: 5 menu items with random quantities
- **Purpose**: Test order history and detail views

### 2. Multiple Reservations Scenario
- **User**: `reservation_test_user`
- **Reservations**: 3 reservations with different statuses
  - Pending (2 days ahead)
  - Confirmed (5 days ahead)
  - Confirmed (10 days ahead)
- **Purpose**: Test reservation filtering and management

### 3. Shopping Cart Scenario
- **User**: `cart_test_user`
- **Cart**: Pending order with 4 items
- **Status**: Pending payment
- **Purpose**: Test cart functionality and checkout flow

### 4. Mixed Status Orders Scenario
- **User**: `status_test_user`
- **Orders**: 4 orders with different statuses
  - Processing (Paid)
  - Ready (Paid)
  - Completed (Paid)
  - Cancelled (Refunded)
- **Purpose**: Test order status filtering and display

---

## Test Users

### Default Test Users

When running `create_sample_data --full`, the following users are created:

#### Customer Users

1. **customer1**
   - Email: `customer1@example.com`
   - Password: `testpass123`
   - Role: Customer
   - Has sample orders and reservations

2. **customer2**
   - Email: `customer2@example.com`
   - Password: `testpass123`
   - Role: Customer
   - Has sample orders and reservations

#### Staff User

3. **manager**
   - Email: `manager@restaurant.com`
   - Password: `testpass123`
   - Role: Staff (can access admin and CRUD operations)

### Test Scenario Users

Additional users created by `create_test_scenarios`:

- `order_test_user` - For order testing
- `reservation_test_user` - For reservation testing
- `cart_test_user` - For cart/checkout testing
- `status_test_user` - For order status testing

All test users have password: `testpass123`

---

## Real Data Scenarios

### Scenario 1: New Customer Journey

1. **Registration**
   - Create account at `/accounts/signup/`
   - Verify email (console in development)

2. **Browse Menu**
   - View menu at `/restaurant/menu/`
   - Filter by category
   - Search for items

3. **Add to Cart**
   - View item details
   - Add multiple items with different quantities
   - Update quantities in cart

4. **Checkout**
   - Review order in cart
   - Proceed to checkout
   - Complete payment (use Stripe test card: `4242 4242 4242 4242`)

5. **Order History**
   - View orders at `/restaurant/orders/`
   - Check order details
   - Track order status

### Scenario 2: Reservation Management

1. **Create Reservation**
   - Navigate to `/restaurant/reservations/create/`
   - Fill form with future date
   - Submit reservation

2. **View Reservations**
   - List all reservations
   - Filter by status (Pending, Confirmed, Cancelled)
   - View reservation details

3. **Edit Reservation**
   - Update guest count
   - Modify date/time
   - Add special requests

4. **Cancel Reservation**
   - Cancel future reservations
   - Verify status change

### Scenario 3: Staff Menu Management

1. **Login as Staff**
   - Use `manager` account
   - Access staff features

2. **Create Menu Item**
   - Navigate to `/restaurant/menu/create/`
   - Fill form with details
   - Upload image (optional)
   - Set availability

3. **Edit Menu Item**
   - Update prices
   - Modify descriptions
   - Change availability status

4. **Delete Menu Item**
   - Remove items (soft delete via availability)
   - Confirm deletion

### Scenario 4: Order Processing (Staff)

1. **View All Orders**
   - Access admin panel
   - Filter by status
   - Search orders

2. **Update Order Status**
   - Change from Processing → Ready
   - Mark as Completed
   - Handle cancellations

3. **Order Analytics**
   - View order totals
   - Check payment status
   - Review order history

---

## Data Verification

### Check Database Counts

```python
from restaurant.models import MenuItem, Order, Reservation
from django.contrib.auth.models import User

print(f"Menu Items: {MenuItem.objects.count()}")
print(f"Orders: {Order.objects.count()}")
print(f"Reservations: {Reservation.objects.count()}")
print(f"Users: {User.objects.count()}")
```

### Verify Sample Data

Run the verification script:
```bash
python verify_functionality.py
```

This checks:
- Database model counts
- Model methods functionality
- Form validation
- URL accessibility

---

## Best Practices

### For Development

1. **Use Sample Data**: Always run `create_sample_data --full` after migrations
2. **Test Scenarios**: Create specific scenarios for feature testing
3. **Image Placeholders**: Test with and without images
4. **User Roles**: Test with both customer and staff accounts

### For Production

1. **Real Images**: Upload actual menu item photos
2. **Data Migration**: Use fixtures or management commands
3. **Image Optimization**: Compress images before upload
4. **CDN**: Consider using CDN for image delivery

### For Testing

1. **Isolated Tests**: Each test should be independent
2. **Test Data**: Use factories or fixtures
3. **Cleanup**: Reset database between test runs
4. **Coverage**: Test all user scenarios

---

## Troubleshooting

### Images Not Displaying

1. Check `MEDIA_URL` and `MEDIA_ROOT` in settings
2. Verify `media/` directory exists
3. Ensure images are uploaded correctly
4. Check file permissions

### Sample Data Not Creating

1. Run migrations: `python manage.py migrate`
2. Check for duplicate entries
3. Verify model fields match command data
4. Check console for error messages

### Test Users Can't Login

1. Verify users were created: `User.objects.all()`
2. Check password was set correctly
3. Ensure user is active: `user.is_active = True`
4. Verify email if email verification is enabled

---

## Summary

- ✅ **25 menu items** across 4 categories
- ✅ **Robust image placeholder system** for missing images
- ✅ **Comprehensive test scenarios** for all features
- ✅ **Multiple test users** with different roles
- ✅ **Real-world data scenarios** for testing

The application is ready for comprehensive testing with realistic data and scenarios!













