# Testing Guide - Django Restaurant

This guide provides instructions for testing all functionality in the Django Restaurant application.

## Automated Tests

### Running All Tests
```bash
python manage.py test restaurant.tests
```

### Running Specific Test Suites
```bash
# Model tests
python manage.py test restaurant.tests.MenuItemModelTest
python manage.py test restaurant.tests.OrderModelTest
python manage.py test restaurant.tests.ReservationModelTest

# Form tests
python manage.py test restaurant.tests.MenuItemFormTest
python manage.py test restaurant.tests.ReservationFormTest

# View tests
python manage.py test restaurant.tests.ViewTests

# Custom logic tests
python manage.py test restaurant.tests.CustomLogicTest
```

## Manual Testing Checklist

### 1. User Registration and Login

#### Registration
1. Navigate to `/accounts/signup/`
2. Fill in the registration form:
   - Username
   - Email (enter twice if required)
   - Password (enter twice)
3. Submit the form
4. **Expected**: User is created and logged in automatically, redirected to home page

#### Login
1. Navigate to `/accounts/login/`
2. Enter username/email and password
3. Click "Login"
4. **Expected**: User is logged in and redirected to home page

#### Logout
1. Click on username in navbar
2. Select "Logout"
3. **Expected**: User is logged out and redirected to home page

### 2. Menu Browsing

#### View Menu List
1. Navigate to `/restaurant/menu/`
2. **Expected**: See all available menu items grouped by category
3. Test search functionality
4. Test category filtering
5. **Expected**: Results update correctly

#### View Menu Item Detail
1. Click on any menu item
2. **Expected**: See detailed information, image, price, description
3. Test "Add to Cart" button (requires login)

### 3. Shopping Cart Functionality

#### Add Items to Cart (Requires Login)
1. Login as a user
2. Navigate to menu
3. Click "Add" on multiple items
4. **Expected**: Items are added to cart, success message appears
5. Navigate to `/restaurant/cart/`
6. **Expected**: See all items in cart with quantities and totals

#### Update Cart Items
1. In cart page, change quantity using the number input
2. Click outside or press Enter
3. **Expected**: Quantity updates, total recalculates

#### Remove Items from Cart
1. Click "Remove" button on an item
2. **Expected**: Item is removed, cart updates

### 4. Checkout and Payment

#### Checkout Process (Requires Login)
1. Add items to cart
2. Navigate to `/restaurant/checkout/`
3. **Expected**: See order summary and payment form
4. **Note**: Stripe integration requires API keys to be configured

#### Payment Success
1. Complete payment (or use Stripe test mode)
2. **Expected**: Redirected to success page with order details

#### Payment Cancel
1. Cancel payment process
2. **Expected**: Redirected to cancel page, items remain in cart

### 5. Order Management

#### View Order List
1. Login as a user
2. Navigate to `/restaurant/orders/`
3. **Expected**: See all past orders (excluding pending cart)

#### View Order Details
1. Click "View Details" on any order
2. **Expected**: See complete order information, items, totals, status

### 6. Reservation Management

#### Create Reservation (Requires Login)
1. Login as a user
2. Navigate to `/restaurant/reservations/create/`
3. Fill in the form:
   - Name
   - Phone number
   - Date (future date)
   - Time (between 11:00 AM - 10:00 PM)
   - Number of guests (1-20)
   - Special requests (optional)
4. Submit form
5. **Expected**: Reservation created, redirected to detail page

#### View Reservations
1. Navigate to `/restaurant/reservations/`
2. **Expected**: See all user's reservations
3. Test status filtering (All, Pending, Confirmed, Cancelled)

#### Update Reservation
1. Click "Edit" on a pending/confirmed reservation
2. Modify details
3. Submit
4. **Expected**: Reservation updated successfully

#### Cancel Reservation
1. Click "Cancel" on a reservation
2. Confirm cancellation
3. **Expected**: Reservation status changed to "cancelled"

### 7. Menu Item Management (Staff Only)

#### Create Menu Item
1. Login as staff user
2. Navigate to `/restaurant/menu/create/`
3. Fill in form:
   - Name
   - Description
   - Price (positive number)
   - Category
   - Image (optional)
   - Availability
4. Submit
5. **Expected**: Menu item created, visible in menu list

#### Update Menu Item
1. Navigate to menu item detail page
2. Click "Edit Item"
3. Modify details
4. Submit
5. **Expected**: Changes saved

#### Delete Menu Item
1. Navigate to menu item detail page
2. Click "Delete Item"
3. Confirm deletion
4. **Expected**: Item removed from menu

### 8. Form Validation Testing

#### Menu Item Form
- **Test**: Submit with negative price
  - **Expected**: Validation error
- **Test**: Submit with empty name
  - **Expected**: Validation error
- **Test**: Submit with valid data
  - **Expected**: Form saves successfully

#### Reservation Form
- **Test**: Submit with past date
  - **Expected**: Validation error "Date cannot be in the past"
- **Test**: Submit with time outside business hours
  - **Expected**: Validation error "Reservations available between 11:00 AM and 10:00 PM"
- **Test**: Submit with more than 20 guests
  - **Expected**: Validation error "Number of guests must be between 1 and 20"
- **Test**: Submit with invalid phone number
  - **Expected**: Validation error "Please enter a valid phone number"
- **Test**: Submit with valid data
  - **Expected**: Reservation created

### 9. Authorization Testing

#### Staff-Only Functions
1. Login as regular user (not staff)
2. Try to access:
   - `/restaurant/menu/create/`
   - `/restaurant/menu/<id>/update/`
   - `/restaurant/menu/<id>/delete/`
3. **Expected**: Redirected (403 or login page)

#### Login-Required Functions
1. Logout
2. Try to access:
   - `/restaurant/cart/`
   - `/restaurant/checkout/`
   - `/restaurant/orders/`
   - `/restaurant/reservations/create/`
3. **Expected**: Redirected to login page

### 10. Custom Logic Testing

The test suite includes tests for:
- Menu filtering by category (using loops and conditionals)
- Order total calculation (using loops)
- Reservation status filtering (using loops and conditionals)

These demonstrate the use of compound statements (if/else, loops) in Python.

## Test Data

### Create Sample Menu Items
```bash
python manage.py create_sample_data
```

This creates 12 sample menu items across all categories for testing.

### Create Test Users
```bash
python manage.py createsuperuser
```

Create a staff user for testing admin functions.

## Common Issues and Solutions

### Issue: Tests fail with database errors
**Solution**: Tests use an in-memory database, so this shouldn't happen. If it does, check migrations are up to date.

### Issue: Stripe payment not working
**Solution**: 
1. Ensure Stripe API keys are set in environment variables
2. Use Stripe test keys for development
3. Check Stripe dashboard for test mode

### Issue: Forms not validating correctly
**Solution**: Check form validation methods in `restaurant/forms.py`

### Issue: Images not displaying
**Solution**: 
1. Ensure `MEDIA_ROOT` and `MEDIA_URL` are configured
2. Run `python manage.py collectstatic` for production
3. Check file permissions

## Test Coverage

Current test coverage includes:
- ✅ Model creation and relationships
- ✅ Form validation
- ✅ View authorization
- ✅ CRUD operations
- ✅ Custom Python logic (loops, conditionals)
- ✅ Cart functionality
- ✅ Order management
- ✅ Reservation management

## Performance Testing

For production, consider testing:
- Page load times
- Database query optimization
- Image loading performance
- Concurrent user handling

## Security Testing

Verify:
- ✅ CSRF protection is enabled
- ✅ SQL injection protection (Django ORM)
- ✅ XSS protection (template escaping)
- ✅ Authentication required for sensitive operations
- ✅ Staff-only access enforced
- ✅ Environment variables for secrets













