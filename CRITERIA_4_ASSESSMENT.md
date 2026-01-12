# Criteria 4 Assessment: E-commerce Payment System

## Criteria 4: Design, develop and integrate an e-commerce payment system in a cloud-hosted Full Stack web application.

---

### 4.1 Implement at least one Django app containing some e-commerce functionality using an online payment processing system (e.g. Stripe). This may be a shopping cart checkout, subscription-based payments or single payments, donations, etc. ✅ **DONE**

**Evidence:**

#### E-commerce Functionality Implementation

The application implements a **complete shopping cart checkout system** using **Stripe** as the online payment processing system.

**Django App**: `restaurant/` app contains all e-commerce functionality

**Payment System**: Stripe (version 10.0.0) - installed and configured

**E-commerce Features Implemented:**
1. ✅ Shopping cart functionality
2. ✅ Add items to cart
3. ✅ Update cart quantities
4. ✅ Remove items from cart
5. ✅ Checkout process
6. ✅ Stripe payment integration
7. ✅ Order management
8. ✅ Payment verification

#### Stripe Integration

**1. Stripe Installation** (`requirements.txt`):
```python
stripe==10.0.0
```

**2. Stripe Configuration** (`flavour/settings.py`):
```python
# Stripe settings (set in environment variables)
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
```

**3. Stripe Import and Setup** (`restaurant/views.py`):
```python
try:
    import stripe
    stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
except ImportError:
    stripe = None
```

#### Shopping Cart Checkout Flow

**Step 1: Add Items to Cart** (`restaurant/views.py` - `add_to_cart`):
```python
@login_required
def add_to_cart(request):
    """Add item to shopping cart."""
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            menu_item_id = form.cleaned_data['menu_item_id']
            quantity = form.cleaned_data['quantity']
            
            # Get or create cart (pending order)
            cart, created = Order.objects.get_or_create(
                user=request.user,
                status='pending',
                payment_status='pending',
                defaults={'order_number': f'CART-{uuid.uuid4().hex[:8].upper()}'}
            )
            
            # Add or update order item
            order_item, created = OrderItem.objects.get_or_create(
                order=cart,
                menu_item=menu_item,
                defaults={'quantity': quantity, 'price': menu_item.price}
            )
            
            if not created:
                order_item.quantity += quantity
                order_item.save()
            
            cart.calculate_total()
            messages.success(request, f'✓ Added {quantity}x {menu_item.name} to cart!')
            return redirect('restaurant:menu_list')
```

**Step 2: View Cart** (`restaurant/views.py` - `cart`):
```python
@login_required
def cart(request):
    """View shopping cart."""
    try:
        cart = Order.objects.get(user=request.user, status='pending', payment_status='pending')
        order_items = cart.order_items.all()
        cart.calculate_total()
    except Order.DoesNotExist:
        cart = None
        order_items = []
    
    return render(request, 'restaurant/cart.html', {'cart': cart, 'order_items': order_items})
```

**Step 3: Checkout - Create Payment Intent** (`restaurant/views.py` - `checkout`):
```python
@login_required
def checkout(request):
    """Checkout view - create payment intent with Stripe."""
    try:
        cart = Order.objects.get(user=request.user, status='pending', payment_status='pending')
        order_items = cart.order_items.all()
    except Order.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('restaurant:cart')
    
    if not order_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('restaurant:cart')
    
    # Calculate total
    total_amount = cart.calculate_total()
    
    # Create Stripe payment intent
    if not stripe:
        messages.error(request, 'Payment system is not available. Please contact support.')
        return redirect('restaurant:cart')
    
    stripe_secret_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
    stripe_publishable_key = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
    
    if not stripe_secret_key or not stripe_publishable_key:
        messages.error(request, 'Payment system is not configured. Please contact support.')
        return redirect('restaurant:cart')
    
    try:
        # Convert to cents for Stripe
        amount_in_cents = int(total_amount * 100)
        
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency='gbp',
            metadata={
                'order_number': cart.order_number,
                'user_id': str(request.user.id),
            }
        )
        
        cart.stripe_payment_intent_id = payment_intent.id
        cart.save()
        
        context = {
            'cart': cart,
            'order_items': order_items,
            'total_amount': total_amount,
            'stripe_publishable_key': stripe_publishable_key,
            'client_secret': payment_intent.client_secret,
        }
        return render(request, 'restaurant/checkout.html', context)
    
    except stripe.error.StripeError as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('restaurant:cart')
```

**Step 4: Stripe Elements Integration** (`restaurant/templates/restaurant/checkout.html`):

**Frontend Stripe Integration:**
```javascript
// Load Stripe.js library
<script src="https://js.stripe.com/v3/"></script>

// Initialize Stripe
window.stripe = Stripe(stripePublishableKey);
window.elements = stripe.elements({
    clientSecret: clientSecret,
    appearance: {
        theme: 'stripe',
        variables: {
            colorPrimary: '#c41e3a',
            // ... custom styling
        }
    }
});

// Create and mount payment element
window.paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');
```

**Step 5: Payment Confirmation** (`restaurant/templates/restaurant/checkout.html`):
```javascript
// Handle form submission
const {error, paymentIntent} = await window.stripe.confirmPayment({
    elements: window.elements,
    confirmParams: {
        return_url: '{{ request.scheme }}://{{ request.get_host }}{% url "restaurant:payment_success" %}?payment_intent={PAYMENT_INTENT_ID}',
    },
    redirect: 'if_required'
});

if (error) {
    // Show error message
    paymentMessage.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-exclamation-circle me-2"></i>
            <span><strong>Payment Error:</strong> ${error.message}</span>
        </div>
    `;
    paymentMessage.className = 'alert alert-danger';
} else if (paymentIntent) {
    // Payment successful
    window.location.href = '{% url "restaurant:payment_success" %}?payment_intent=' + paymentIntent.id;
}
```

#### Order Model with Payment Tracking

**Order Model** (`restaurant/models.py`):
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
    # ... other fields
```

**Key Features:**
- ✅ Tracks payment status (pending, paid, failed, refunded)
- ✅ Stores Stripe payment intent ID for verification
- ✅ Tracks order status through fulfillment process
- ✅ Calculates total amount automatically

#### URL Configuration

**Payment URLs** (`restaurant/urls.py`):
```python
urlpatterns = [
    # Cart and checkout
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/item/<int:item_id>/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/item/<int:item_id>/remove/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
]
```

#### Complete E-commerce Flow

1. **Browse Menu** → User views available menu items
2. **Add to Cart** → User adds items to shopping cart (creates Order with status='pending')
3. **View Cart** → User reviews cart items and quantities
4. **Update Cart** → User can modify quantities or remove items
5. **Proceed to Checkout** → User clicks checkout button
6. **Payment Intent Created** → Server creates Stripe PaymentIntent
7. **Enter Card Details** → Stripe Elements provides secure card input
8. **Process Payment** → Stripe processes payment securely
9. **Payment Verification** → Server verifies payment with Stripe
10. **Order Confirmation** → Order status updated to 'processing', payment_status to 'paid'
11. **Order Tracking** → User can view order history and details

**Files:**
- `restaurant/views.py` - All e-commerce views (Lines 155-400)
- `restaurant/models.py` - Order and OrderItem models (Lines 77-212)
- `restaurant/templates/restaurant/checkout.html` - Checkout page with Stripe integration
- `restaurant/templates/restaurant/cart.html` - Shopping cart page
- `restaurant/urls.py` - E-commerce URLs
- `requirements.txt` - Stripe dependency (Line 10)
- `flavour/settings.py` - Stripe configuration (Lines 194-197)

---

### 4.2 Implement a feedback system that reports successful and unsuccessful purchases to the user, with a helpful message ✅ **DONE**

**Evidence:**

#### Comprehensive Feedback System

The application implements a **multi-layered feedback system** that provides clear, helpful messages for all payment outcomes:

**1. Payment Success Feedback**

**Success View** (`restaurant/views.py` - `payment_success`):
```python
@login_required
def payment_success(request):
    """Handle successful payment."""
    payment_intent_id = request.GET.get('payment_intent')
    order = None
    
    if payment_intent_id:
        try:
            order = Order.objects.get(
                user=request.user,
                stripe_payment_intent_id=payment_intent_id
            )
            
            # Verify payment with Stripe
            if stripe:
                try:
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                    
                    if payment_intent.status == 'succeeded':
                        order.payment_status = 'paid'
                        order.status = 'processing'
                        order.save()
                        messages.success(request, f'Payment successful! Order #{order.order_number} is being processed.')
                    else:
                        messages.error(request, 'Payment was not successful. Please try again.')
                        return redirect('restaurant:checkout')
                except stripe.error.StripeError as e:
                    messages.error(request, f'Payment verification error: {str(e)}')
            else:
                # If Stripe is not available, assume payment succeeded (for testing)
                order.payment_status = 'paid'
                order.status = 'processing'
                order.save()
                messages.success(request, f'Payment successful! Order #{order.order_number} is being processed.')
        
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
    
    context = {
        'order': order,
    }
    return render(request, 'restaurant/payment_success.html', context)
```

**Success Page Template** (`restaurant/templates/restaurant/payment_success.html`):
```html
<div class="card shadow-lg text-center">
    <div class="card-body p-5">
        <div class="mb-4">
            <div class="success-icon mx-auto mb-3">
                <i class="fas fa-check-circle"></i>
            </div>
            <h2 class="text-success mb-3">Payment Successful!</h2>
            <p class="lead text-muted">
                Thank you for your order. Your payment has been processed successfully.
            </p>
        </div>
        
        {% if order %}
        <div class="alert alert-success mb-4">
            <div class="d-flex align-items-center justify-content-center">
                <i class="fas fa-receipt fa-2x me-3"></i>
                <div class="text-start">
                    <strong>Order Number:</strong> {{ order.order_number }}<br>
                    <strong>Total Amount:</strong> £{{ order.total_amount }}
                </div>
            </div>
        </div>
        
        <div class="mb-4">
            <p class="text-muted">
                Your order is being processed and you will receive a confirmation email shortly.
                You can track your order status in your order history.
            </p>
        </div>
        
        <div class="d-flex gap-3 justify-content-center">
            <a href="{% url 'restaurant:order_detail' order.pk %}" class="btn btn-primary btn-lg">
                <i class="fas fa-eye me-2"></i>View Order Details
            </a>
            <a href="{% url 'restaurant:order_list' %}" class="btn btn-outline-primary btn-lg">
                <i class="fas fa-list me-2"></i>My Orders
            </a>
        </div>
        {% endif %}
    </div>
</div>
```

**Success Feedback Features:**
- ✅ Visual success icon (green checkmark)
- ✅ Clear success message
- ✅ Order number and total amount displayed
- ✅ Next steps guidance (track order, view details)
- ✅ Action buttons (View Order Details, My Orders)
- ✅ Django messages.success() for additional feedback

**2. Payment Cancellation Feedback**

**Cancel View** (`restaurant/views.py` - `payment_cancel`):
```python
@login_required
def payment_cancel(request):
    """Handle cancelled payment."""
    messages.info(request, 'Payment was cancelled. Your items are still in your cart.')
    return render(request, 'restaurant/payment_cancel.html')
```

**Cancel Page Template** (`restaurant/templates/restaurant/payment_cancel.html`):
```html
<div class="card shadow-lg text-center">
    <div class="card-body p-5">
        <div class="mb-4">
            <div class="cancel-icon mx-auto mb-3">
                <i class="fas fa-times-circle"></i>
            </div>
            <h2 class="text-warning mb-3">Payment Cancelled</h2>
            <p class="lead text-muted">
                Your payment was cancelled. No charges have been made to your account.
            </p>
        </div>
        
        <div class="alert alert-info mb-4">
            <div class="d-flex align-items-center">
                <i class="fas fa-info-circle fa-2x me-3"></i>
                <div class="text-start">
                    <strong>What happened?</strong>
                    <p class="mb-0 small">You cancelled the payment process. Your items are still in your cart and you can complete your order anytime.</p>
                </div>
            </div>
        </div>
        
        <div class="d-flex gap-3 justify-content-center">
            <a href="{% url 'restaurant:cart' %}" class="btn btn-primary btn-lg">
                <i class="fas fa-shopping-cart me-2"></i>Return to Cart
            </a>
            <a href="{% url 'restaurant:menu_list' %}" class="btn btn-outline-primary btn-lg">
                <i class="fas fa-utensils me-2"></i>Continue Shopping
            </a>
        </div>
    </div>
</div>
```

**Cancellation Feedback Features:**
- ✅ Visual cancellation icon (orange warning)
- ✅ Clear cancellation message
- ✅ Reassurance (no charges made)
- ✅ Explanation of what happened
- ✅ Action buttons (Return to Cart, Continue Shopping)
- ✅ Django messages.info() for additional feedback

**3. Payment Error Feedback**

**Error Handling in Checkout** (`restaurant/views.py` - `checkout`):
```python
except stripe.error.StripeError as e:
    messages.error(request, f'Payment error: {str(e)}')
    return redirect('restaurant:cart')
```

**Error Handling in Payment Success** (`restaurant/views.py` - `payment_success`):
```python
except stripe.error.StripeError as e:
    messages.error(request, f'Payment verification error: {str(e)}')
```

**Frontend Error Feedback** (`restaurant/templates/restaurant/checkout.html`):
```javascript
if (error) {
    // Show error message
    paymentMessage.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-exclamation-circle me-2"></i>
            <span><strong>Payment Error:</strong> ${error.message}</span>
        </div>
    `;
    paymentMessage.className = 'alert alert-danger';
    
    // Re-enable form
    submitButton.disabled = false;
    submitButton.classList.remove('payment-loading');
    
    // Scroll to error message
    paymentMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
```

**Error Feedback Features:**
- ✅ Clear error messages with specific error details
- ✅ Visual error indicators (red alert, exclamation icon)
- ✅ Form remains accessible (user can retry)
- ✅ Error messages scroll into view
- ✅ Django messages.error() for persistent feedback

**4. Payment Status Feedback**

**Payment Status Messages:**
```python
# Payment not successful
messages.error(request, 'Payment was not successful. Please try again.')

# Payment verification error
messages.error(request, f'Payment verification error: {str(e)}')

# Order not found
messages.error(request, 'Order not found.')

# Payment system not available
messages.error(request, 'Payment system is not available. Please contact support.')

# Payment system not configured
messages.error(request, 'Payment system is not configured. Please contact support.')
```

**5. Real-time Payment Feedback**

**Payment Processing States** (`restaurant/templates/restaurant/checkout.html`):
```javascript
// Loading state
submitButton.disabled = true;
submitButton.classList.add('payment-loading');
buttonText.style.display = 'none';
spinner.classList.remove('d-none');

// Success state
paymentMessage.innerHTML = `
    <div class="d-flex align-items-center">
        <i class="fas fa-check-circle me-2"></i>
        <span><strong>Payment Successful!</strong> Redirecting...</span>
    </div>
`;
paymentMessage.className = 'alert alert-success';

// Requires action (3D Secure)
paymentMessage.innerHTML = `
    <div class="d-flex align-items-center">
        <i class="fas fa-info-circle me-2"></i>
        <span>Please complete the additional authentication step.</span>
    </div>
`;
paymentMessage.className = 'alert alert-info';

// Processing state
paymentMessage.innerHTML = `
    <div class="d-flex align-items-center">
        <i class="fas fa-clock me-2"></i>
        <span>Payment is being processed. Please wait...</span>
    </div>
`;
paymentMessage.className = 'alert alert-info';
```

**Real-time Feedback Features:**
- ✅ Loading spinner during payment processing
- ✅ Button disabled during processing
- ✅ Status messages for different payment states
- ✅ Visual indicators (icons, colors)
- ✅ Automatic redirect on success

**6. Django Messages Framework**

**Message Display** (`templates/base.html`):
```html
{% if messages %}
<div class="container mt-4">
    {% for message in messages %}
    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
        {{ message }}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    {% endfor %}
</div>
{% endif %}
```

**Message Types Used:**
- `messages.success()` - Payment successful, order created, etc.
- `messages.error()` - Payment errors, validation errors, etc.
- `messages.info()` - Payment cancelled, informational messages
- `messages.warning()` - Warnings (if needed)

#### Feedback System Summary

| Payment Outcome | Feedback Method | Message Type | User Action |
|----------------|-----------------|--------------|-------------|
| **Success** | Success page + Django message | Success | View order details, track order |
| **Cancelled** | Cancel page + Django message | Info | Return to cart, continue shopping |
| **Error** | Error message + Django message | Error | Retry payment, contact support |
| **Processing** | Loading state + status message | Info | Wait for processing |
| **Requires Action** | Info message (3D Secure) | Info | Complete authentication |

**Files:**
- `restaurant/views.py` - Payment success/cancel views (Lines 328-375)
- `restaurant/templates/restaurant/payment_success.html` - Success page template
- `restaurant/templates/restaurant/payment_cancel.html` - Cancel page template
- `restaurant/templates/restaurant/checkout.html` - Error handling in checkout (Lines 461-515)
- `templates/base.html` - Django messages display

---

## Summary

### ✅ ALL CRITERIA MET - **DONE**

| Criterion | Status | Evidence |
|-----------|--------|----------|
| 4.1 Implement e-commerce functionality with online payment system | ✅ DONE | Stripe integration, shopping cart checkout, PaymentIntent creation, secure payment processing |
| 4.2 Implement feedback system for successful/unsuccessful purchases | ✅ DONE | Success page, cancel page, error messages, real-time feedback, Django messages |

---

## Additional E-commerce Features

1. **Cart Management:**
   - Add items to cart
   - Update quantities
   - Remove items
   - Calculate totals automatically

2. **Order Tracking:**
   - Order history
   - Order details with items
   - Order status tracking
   - Invoice download (for paid orders)

3. **Security:**
   - Stripe Elements (PCI compliant)
   - Secure payment processing
   - Payment verification
   - No card details stored on server

4. **User Experience:**
   - Professional checkout UI
   - Loading states
   - Error handling
   - Clear navigation paths

5. **Payment Features:**
   - Multiple payment methods (via Stripe)
   - 3D Secure support
   - Payment verification
   - Order metadata tracking

---

## Conclusion

**The project fully meets all 2 assessment criteria for Criteria 4.** The application implements a complete e-commerce shopping cart checkout system using Stripe as the online payment processing system. The checkout flow includes cart management, secure payment processing through Stripe Elements, and comprehensive feedback for all payment outcomes (success, cancellation, errors). The feedback system provides clear, helpful messages with visual indicators, actionable next steps, and uses Django's messages framework for persistent notifications. All payment processing is secure, PCI-compliant through Stripe, and properly integrated into the Django application.




