# Criteria 2 Assessment: Relational Data Model and Business Logic

## Criteria 2: Design and implement a relational data model, application features and business logic to manage, query and manipulate relational data to meet given needs in a particular real-world domain.

---

### 2.1 Design a relational database schema with clear relationships between entities ✅ **DONE**

**Evidence:**

#### Database Schema Overview

The application implements a well-designed relational database schema for a restaurant management system with the following entities and relationships:

**Entity Relationship Diagram:**
```
User (Django built-in)
    │
    ├─── Order (1:Many) ──── OrderItem (1:Many)
    │         │                    │
    │         │                    └─── MenuItem (Many:1)
    │         │
    └─── Reservation (1:Many)
```

#### Detailed Relationships

1. **User → Order (One-to-Many)**
   ```python
   # In Order model
   user = models.ForeignKey(
       User,
       on_delete=models.CASCADE,
       related_name='orders',
       help_text="User who placed the order"
   )
   ```
   - **Relationship Type**: One-to-Many (One User can have many Orders)
   - **Delete Behavior**: CASCADE (if User is deleted, all their Orders are deleted)
   - **Related Name**: `orders` (allows `user.orders.all()`)

2. **Order → OrderItem (One-to-Many)**
   ```python
   # In OrderItem model
   order = models.ForeignKey(
       Order,
       on_delete=models.CASCADE,
       related_name='order_items',
       help_text="Order this item belongs to"
   )
   ```
   - **Relationship Type**: One-to-Many (One Order can have many OrderItems)
   - **Delete Behavior**: CASCADE (if Order is deleted, all OrderItems are deleted)
   - **Related Name**: `order_items` (allows `order.order_items.all()`)

3. **MenuItem → OrderItem (One-to-Many)**
   ```python
   # In OrderItem model
   menu_item = models.ForeignKey(
       MenuItem,
       on_delete=models.CASCADE,
       help_text="Menu item ordered"
   )
   ```
   - **Relationship Type**: One-to-Many (One MenuItem can appear in many OrderItems)
   - **Delete Behavior**: CASCADE (if MenuItem is deleted, all related OrderItems are deleted)

4. **User → Reservation (One-to-Many)**
   ```python
   # In Reservation model
   user = models.ForeignKey(
       User,
       on_delete=models.CASCADE,
       related_name='reservations',
       help_text="User who made the reservation"
   )
   ```
   - **Relationship Type**: One-to-Many (One User can have many Reservations)
   - **Delete Behavior**: CASCADE (if User is deleted, all their Reservations are deleted)
   - **Related Name**: `reservations` (allows `user.reservations.all()`)

#### Schema Design Principles

✅ **Normalization**: 
- Data is properly normalized (no redundant data)
- OrderItem stores price snapshot (price at time of order) to prevent historical data issues

✅ **Referential Integrity**:
- All ForeignKeys use `on_delete=models.CASCADE` for data consistency
- Unique constraints where appropriate (`order_number` is unique)

✅ **Clear Naming**:
- Model names are descriptive (MenuItem, Order, OrderItem, Reservation)
- Field names are clear and follow Django conventions
- Related names are explicit (`orders`, `order_items`, `reservations`)

✅ **Business Logic in Models**:
- `Order.calculate_total()` - Calculates total from order items
- `OrderItem.save()` - Auto-calculates subtotal and updates order total

**Files:**
- `restaurant/models.py` - Complete schema definition (Lines 7-279)
- `restaurant/migrations/0001_initial.py` and `0002_order_orderitem_reservation.py` - Database migrations

---

### 2.2 Create at least TWO original custom Django models ✅ **DONE**

**Evidence:**

The application includes **FOUR original custom Django models** (exceeding the requirement of at least two):

#### 1. MenuItem Model
```python
class MenuItem(models.Model):
    """
    Model representing a menu item in the restaurant.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
```

**Features:**
- Custom fields: name, description, price, category, image, is_available
- Custom choices: CATEGORY_CHOICES (appetizer, main, dessert, drink)
- Custom Meta class with ordering and verbose names
- Custom `__str__` method

#### 2. Order Model
```python
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_address = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_total(self):
        """Calculate total amount from order items."""
        total = Decimal('0.00')
        for item in self.order_items.all():
            total += item.subtotal
        self.total_amount = total
        self.save()
        return total
    
    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"
```

**Features:**
- Custom fields: order_number, status, payment_status, total_amount, etc.
- Custom choices: STATUS_CHOICES and PAYMENT_STATUS_CHOICES
- Custom method: `calculate_total()` - business logic for order totals
- ForeignKey relationship to User
- Custom Meta class with ordering

#### 3. OrderItem Model
```python
class OrderItem(models.Model):
    """
    Model representing an item in an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        """Calculate subtotal before saving."""
        if not self.price:
            self.price = self.menu_item.price
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)
        # Update order total
        self.order.calculate_total()
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} in Order {self.order.order_number}"
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
```

**Features:**
- Custom fields: quantity, price, subtotal
- Custom `save()` method override - auto-calculates subtotal and updates order total
- ForeignKey relationships to Order and MenuItem
- Validators: MinValueValidator(1) for quantity

#### 4. Reservation Model
```python
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reservation for {self.name} on {self.date} at {self.time}"
    
    class Meta:
        ordering = ['date', 'time']
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
```

**Features:**
- Custom fields: name, email, phone, date, time, number_of_guests, special_requests, status
- Custom choices: STATUS_CHOICES
- Validators: MinValueValidator(1), MaxValueValidator(20) for number_of_guests
- ForeignKey relationship to User
- Custom Meta class with ordering

**All models are:**
- ✅ Original (not Django built-in models)
- ✅ Custom-designed for the restaurant domain
- ✅ Include custom fields, methods, and business logic
- ✅ Properly documented with docstrings

**Files:**
- `restaurant/models.py` - All four custom models (Lines 7-279)

---

### 2.3 Create at least one form with validation that will allow users to create records in the database (in addition to the authentication mechanism) ✅ **DONE**

**Evidence:**

The application includes **MULTIPLE forms with validation** that allow users to create records (exceeding the requirement):

#### 1. MenuItemForm - Creates MenuItem Records
```python
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
            # ... other widgets
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
```

**Usage:**
- **View**: `menu_item_create` (staff only)
- **URL**: `/restaurant/menu/create/`
- **Creates**: MenuItem records in database
- **Validation**: 
  - Price must be > 0
  - Name cannot be empty
  - All required fields validated

#### 2. ReservationForm - Creates Reservation Records
```python
class ReservationForm(forms.ModelForm):
    """
    Form for creating table reservations.
    Includes validation for date, time, and number of guests.
    """
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'date', 'time', 'number_of_guests', 'special_requests']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': timezone.now().date().isoformat()
            }),
            # ... other widgets
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
```

**Usage:**
- **View**: `reservation_create` (login required)
- **URL**: `/restaurant/reservations/create/`
- **Creates**: Reservation records in database
- **Validation**: 
  - Date must be in future (not past)
  - Date cannot be more than 3 months ahead
  - Time must be between 11:00 AM - 10:00 PM
  - Number of guests must be 1-20
  - Phone number format validation

#### 3. OrderItemForm - Creates OrderItem Records (via Cart)
```python
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
```

**Usage:**
- **View**: `add_to_cart` (login required)
- **URL**: `/restaurant/cart/add/`
- **Creates**: OrderItem records (and Order if needed) in database
- **Validation**: Quantity must be 1-10

#### Form Validation Features

✅ **Custom Validation Methods:**
- `clean_price()` - Validates price > 0
- `clean_name()` - Validates name not empty
- `clean_date()` - Validates date in future, max 3 months
- `clean_time()` - Validates business hours
- `clean_number_of_guests()` - Validates guest count 1-20
- `clean_phone()` - Validates phone format
- `clean_quantity()` - Validates quantity 1-10

✅ **Django Built-in Validation:**
- Required fields
- Field type validation (EmailField, DecimalField, etc.)
- Min/Max validators on model fields

✅ **User-Friendly Error Messages:**
- All validation errors provide clear, actionable messages
- Errors displayed in forms using Django's error system

**Files:**
- `restaurant/forms.py` - All form definitions with validation (Lines 8-176)
- `restaurant/views.py` - Form handling views:
  - `menu_item_create` (Lines 95-110)
  - `reservation_create` (Lines 620-638)
  - `add_to_cart` (Lines 155-208)

**Test Evidence:**
- `restaurant/tests.py` - Form validation tests:
  - `MenuItemFormTest` (Lines 125-158)
  - `ReservationFormTest` (Lines 161-201)

---

### 2.4 Implement all CRUD (create, select/read, update, delete) functionality ✅ **DONE**

**Evidence:**

The application implements **complete CRUD functionality** for multiple entities:

#### 1. MenuItem CRUD Operations

**✅ CREATE:**
- **View**: `menu_item_create` (Lines 95-110 in `restaurant/views.py`)
- **URL**: `/restaurant/menu/create/`
- **Method**: GET (form) and POST (submit)
- **Authorization**: Staff only (`@user_passes_test(is_staff_user)`)
- **Form**: `MenuItemForm`
- **Template**: `restaurant/menu_item_form.html`
- **Creates**: New MenuItem records in database

**✅ READ (Select):**
- **List View**: `menu_list` (Lines 47-81 in `restaurant/views.py`)
  - **URL**: `/restaurant/menu/`
  - **Displays**: All available menu items
  - **Features**: Search, category filtering, grouped by category
  
- **Detail View**: `menu_detail` (Lines 84-90 in `restaurant/views.py`)
  - **URL**: `/restaurant/menu/<int:pk>/`
  - **Displays**: Single menu item with full details
  - **Features**: Image display, add to cart form

**✅ UPDATE:**
- **View**: `menu_item_update` (Lines 115-133 in `restaurant/views.py`)
- **URL**: `/restaurant/menu/<int:pk>/update/`
- **Method**: GET (form with existing data) and POST (submit changes)
- **Authorization**: Staff only (`@user_passes_test(is_staff_user)`)
- **Form**: `MenuItemForm` (with instance)
- **Template**: `restaurant/menu_item_form.html`
- **Updates**: Existing MenuItem records in database

**✅ DELETE:**
- **View**: `menu_item_delete` (Lines 138-151 in `restaurant/views.py`)
- **URL**: `/restaurant/menu/<int:pk>/delete/`
- **Method**: GET (confirmation page) and POST (confirm deletion)
- **Authorization**: Staff only (`@user_passes_test(is_staff_user)`)
- **Template**: `restaurant/menu_item_confirm_delete.html`
- **Deletes**: MenuItem records from database
- **Cascade**: Related OrderItems are also deleted (CASCADE)

#### 2. Order CRUD Operations

**✅ CREATE:**
- **View**: `add_to_cart` (Lines 155-208 in `restaurant/views.py`)
- **URL**: `/restaurant/cart/add/`
- **Method**: POST
- **Authorization**: Login required (`@login_required`)
- **Creates**: 
  - Order record (if cart doesn't exist)
  - OrderItem records
- **Business Logic**: 
  - Gets or creates pending order
  - Gets or creates order item (updates quantity if exists)
  - Calculates total

**✅ READ (Select):**
- **List View**: `order_list` (Lines 379-387 in `restaurant/views.py`)
  - **URL**: `/restaurant/orders/`
  - **Displays**: All orders for logged-in user (excluding pending cart)
  - **Template**: `restaurant/order_list.html`
  - **Features**: Status badges, payment status, order history
  
- **Detail View**: `order_detail` (Lines 391-400 in `restaurant/views.py`)
  - **URL**: `/restaurant/orders/<int:pk>/`
  - **Displays**: Single order with all items
  - **Template**: `restaurant/order_detail.html`
  - **Features**: Item details, status tracking, invoice download

- **Cart View**: `cart` (Lines 212-228 in `restaurant/views.py`)
  - **URL**: `/restaurant/cart/`
  - **Displays**: Current shopping cart (pending order)
  - **Template**: `restaurant/cart.html`
  - **Features**: Item management, quantity updates, order summary

**✅ UPDATE:**
- **Cart Item Update**: `update_cart_item` (Lines 232-250 in `restaurant/views.py`)
  - **URL**: `/restaurant/cart/item/<int:item_id>/update/`
  - **Method**: POST
  - **Authorization**: Login required (`@login_required`)
  - **Updates**: OrderItem quantity
  - **Business Logic**: Recalculates order total after update

**✅ DELETE:**
- **Cart Item Remove**: `remove_cart_item` (Lines 254-265 in `restaurant/views.py`)
  - **URL**: `/restaurant/cart/item/<int:item_id>/remove/`
  - **Method**: POST (`@require_POST`)
  - **Authorization**: Login required (`@login_required`)
  - **Deletes**: OrderItem from cart
  - **Business Logic**: Recalculates order total after deletion

#### 3. Reservation CRUD Operations

**✅ CREATE:**
- **View**: `reservation_create` (Lines 620-638 in `restaurant/views.py`)
- **URL**: `/restaurant/reservations/create/`
- **Method**: GET (form) and POST (submit)
- **Authorization**: Login required (`@login_required`)
- **Form**: `ReservationForm`
- **Template**: `restaurant/reservation_form.html`
- **Creates**: New Reservation records in database
- **Business Logic**: Auto-assigns user and email from logged-in user

**✅ READ (Select):**
- **List View**: `reservation_list` (Lines 642-655 in `restaurant/views.py`)
  - **URL**: `/restaurant/reservations/`
  - **Displays**: All reservations for logged-in user
  - **Template**: `restaurant/reservation_list.html`
  - **Features**: Status filtering, card-based layout
  
- **Detail View**: `reservation_detail` (Lines 659-666 in `restaurant/views.py`)
  - **URL**: `/restaurant/reservations/<int:pk>/`
  - **Displays**: Single reservation with full details
  - **Template**: `restaurant/reservation_detail.html`
  - **Features**: Status display, update/cancel buttons

**✅ UPDATE:**
- **View**: `reservation_update` (Lines 670-693 in `restaurant/views.py`)
- **URL**: `/restaurant/reservations/<int:pk>/update/`
- **Method**: GET (form with existing data) and POST (submit changes)
- **Authorization**: Login required (`@login_required`)
- **Form**: `ReservationForm` (with instance)
- **Template**: `restaurant/reservation_form.html`
- **Updates**: Existing Reservation records in database
- **Business Logic**: Prevents updates to cancelled/completed reservations

**✅ DELETE:**
- **View**: `reservation_delete` (Lines 697-710 in `restaurant/views.py`)
- **URL**: `/restaurant/reservations/<int:pk>/delete/`
- **Method**: GET (confirmation page) and POST (confirm cancellation)
- **Authorization**: Login required (`@login_required`)
- **Template**: `restaurant/reservation_confirm_delete.html`
- **Action**: Sets status to 'cancelled' (soft delete pattern)
- **Note**: Uses soft delete (status change) rather than hard delete

#### CRUD Implementation Summary

| Entity | Create | Read | Update | Delete |
|--------|--------|------|--------|--------|
| **MenuItem** | ✅ Staff form | ✅ List + Detail | ✅ Staff form | ✅ Staff confirmation |
| **Order** | ✅ Via cart | ✅ List + Detail | ✅ Cart items | ✅ Cart items |
| **Reservation** | ✅ User form | ✅ List + Detail | ✅ User form | ✅ Cancel (soft) |

#### Additional CRUD Features

✅ **Django Admin Interface:**
- All models registered in admin (`restaurant/admin.py`)
- Inline editing for OrderItems within Orders
- List filters, search, and bulk actions
- Custom admin methods (image preview, has_image)

✅ **Query Operations:**
- Filtering: Menu items by category, availability
- Searching: Menu items by name/description
- Ordering: Custom ordering in Meta classes
- Aggregations: Order total calculation

✅ **Business Logic:**
- Order total calculation (automatic)
- OrderItem subtotal calculation (automatic)
- Cart management (get or create pattern)
- Status management (Order and Reservation statuses)

**Files:**
- `restaurant/views.py` - All CRUD views
- `restaurant/urls.py` - All CRUD URLs
- `restaurant/admin.py` - Admin CRUD interface
- `restaurant/templates/restaurant/*.html` - All CRUD templates

**Test Evidence:**
- `restaurant/tests.py` - CRUD operation tests:
  - `ViewTests.test_menu_item_create_requires_staff` (Lines 239-253)
  - `ViewTests.test_menu_item_update_requires_staff` (Lines 255-263)
  - `ViewTests.test_add_to_cart_creates_order` (Lines 328-348)
  - `ViewTests.test_update_cart_item` (Lines 350-375)
  - `ViewTests.test_remove_cart_item` (Lines 377-398)
  - `ViewTests.test_reservation_form_submission` (Lines 400-429)

---

## Summary

### ✅ ALL CRITERIA MET - **DONE**

| Criterion | Status | Evidence |
|-----------|--------|----------|
| 2.1 Design relational database schema with clear relationships | ✅ DONE | 4 ForeignKey relationships, CASCADE deletes, related_names, normalized schema |
| 2.2 Create at least TWO original custom Django models | ✅ DONE | 4 custom models: MenuItem, Order, OrderItem, Reservation (exceeds requirement) |
| 2.3 Create at least one form with validation for creating records | ✅ DONE | 3 forms: MenuItemForm, ReservationForm, OrderItemForm (exceeds requirement) |
| 2.4 Implement all CRUD functionality | ✅ DONE | Complete CRUD for MenuItem, Order, Reservation with proper authorization |

---

## Additional Strengths

1. **Business Logic in Models:**
   - `Order.calculate_total()` - Automatic total calculation
   - `OrderItem.save()` - Automatic subtotal calculation and order update
   - Custom validation in forms

2. **Data Integrity:**
   - CASCADE deletes maintain referential integrity
   - Price snapshots in OrderItem (historical accuracy)
   - Unique constraints (order_number)

3. **Query Optimization:**
   - Proper use of `select_related` and `prefetch_related` (where applicable)
   - Efficient filtering and searching
   - Custom ordering in Meta classes

4. **Authorization:**
   - Staff-only CRUD for MenuItem
   - User-specific CRUD for Orders and Reservations
   - Login requirements enforced

5. **User Experience:**
   - Soft delete for Reservations (status change)
   - Confirmation pages for deletions
   - Clear error messages and validation feedback

---

## Conclusion

**The project fully meets all 4 assessment criteria for Criteria 2.** The application implements a well-designed relational database schema with clear relationships, multiple original custom models, comprehensive forms with validation, and complete CRUD functionality for all major entities. The business logic is properly implemented in models and views, ensuring data integrity and providing a solid foundation for the restaurant management system.




