# Payment Flow Explanation

## How Card Payment Works

### 1. **Customer Journey**
When a customer clicks "Proceed to Checkout":

1. **Cart Page** → Customer reviews items and clicks "Proceed to Checkout"
2. **Checkout Page** → Customer sees:
   - Order summary (items, quantities, total)
   - **Card Details section** (where they enter payment info)
   - "Pay £X.XX" button

### 2. **Card Input Fields**
The card input fields are **automatically created by Stripe Elements** when the checkout page loads. These fields include:

- **Card Number** field
- **Expiry Date** field (MM/YY)
- **CVC** field (3-4 digits)
- **ZIP/Postal Code** field (if required)

These fields appear in the `#payment-element` div on the checkout page.

### 3. **What Happens When Customer Enters Card Details**

1. **Customer fills in card details** in the Stripe Elements form
2. **Customer clicks "Pay £X.XX" button**
3. **Stripe validates** the card details
4. **Payment is processed** securely through Stripe
5. **Customer is redirected** to:
   - **Success page** if payment succeeds
   - **Cancel page** if payment is cancelled
   - **Error message** if payment fails

### 4. **Test Mode**
When using Stripe test mode, customers can use:

- **Card Number:** `4242 4242 4242 4242`
- **Expiry:** Any future date (e.g., 12/25)
- **CVC:** Any 3 digits (e.g., 123)
- **ZIP:** Any 5 digits (e.g., 12345)

### 5. **Security**
- Card details are **never stored** on your server
- All payment processing happens through **Stripe's secure servers**
- The checkout page uses **HTTPS** (in production)
- Stripe Elements provides **PCI compliance** automatically

## Troubleshooting

### If card input fields don't appear:

1. **Check Stripe keys** in `.env` file:
   ```
   STRIPE_SECRET_KEY=pk_test_...
   STRIPE_PUBLISHABLE_KEY=sk_test_...
   ```

2. **Restart Django server** after updating `.env`:
   ```bash
   # Stop server (Ctrl+C)
   python manage.py runserver
   ```

3. **Check browser console** (F12 → Console) for errors

4. **Verify you're logged in** (checkout requires authentication)

5. **Check that cart has items** (empty cart redirects back)

### If "Pay" button doesn't work:

1. **Check browser console** for JavaScript errors
2. **Verify Stripe.js is loading** (check Network tab)
3. **Check if payment element is mounted** (should see card fields)
4. **Verify you have items in cart**

## Visual Flow

```
Cart Page
    ↓
[Proceed to Checkout Button]
    ↓
Checkout Page
    ├── Order Summary (left side)
    └── Payment Form (right side)
        ├── Card Details Section
        │   ├── Card Number: [____ ____ ____ ____]
        │   ├── Expiry: [MM/YY]
        │   ├── CVC: [___]
        │   └── ZIP: [_____]
        └── [Pay £X.XX Button]
            ↓
        Payment Processing
            ↓
        Success/Cancel Page
```

## Key Points

✅ **Card input fields appear automatically** when Stripe Elements loads  
✅ **No manual form creation needed** - Stripe handles it  
✅ **Secure by default** - PCI compliant  
✅ **Works in test mode** with test card numbers  
✅ **Real-time validation** - errors shown as customer types  

## Next Steps

1. **Get Stripe API keys** from https://dashboard.stripe.com/test/apikeys
2. **Add keys to `.env` file**
3. **Restart Django server**
4. **Test with test card:** `4242 4242 4242 4242`
5. **Go live** by switching to live API keys in production









