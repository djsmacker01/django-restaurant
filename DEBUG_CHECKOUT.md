# Debugging "Proceed to Checkout" Issue

## Common Reasons Why Checkout Button Doesn't Work

### 1. Stripe Keys Not Configured (Most Common)

**Symptom**: Button appears to do nothing, or you get redirected back to cart with error message.

**Check**: Open your `.env` file and verify:
- `STRIPE_SECRET_KEY` has a real key (not placeholder)
- `STRIPE_PUBLISHABLE_KEY` has a real key (not placeholder)
- Keys start with `sk_test_` and `pk_test_` (for test mode)

**Solution**: 
1. Get keys from https://dashboard.stripe.com/test/apikeys
2. Update `.env` file with real keys
3. Restart Django server

### 2. Check Browser Console for Errors

**How to check**:
1. Open browser (Chrome/Firefox)
2. Press F12 to open Developer Tools
3. Click "Console" tab
4. Click "Proceed to Checkout" button
5. Look for any red error messages

**Common errors**:
- `Stripe is not defined` - Stripe.js not loading
- `Invalid API key` - Wrong Stripe key format
- `CORS error` - Network/security issue

### 3. Check Django Server Console

**What to look for**:
- Error messages when clicking checkout
- Messages like "Payment system is not configured"
- Any traceback/error output

### 4. Verify You're Logged In

The checkout requires login. If not logged in:
- You'll be redirected to login page
- After login, you'll be redirected back

### 5. Check Cart Has Items

**Verify**:
- Cart has at least one item
- Total amount is greater than £0.00
- Items are actually in the cart

### 6. Check URL Routing

**Test the URL directly**:
- Try visiting: http://127.0.0.1:8000/restaurant/checkout/
- If it works, the button link might have an issue
- If it doesn't, there's a server-side issue

## Quick Diagnostic Steps

1. **Check .env file**:
   ```bash
   cat .env | grep STRIPE
   ```
   Should show actual keys, not placeholders

2. **Check if logged in**:
   - Look for your username in navbar
   - If not, click "Login" first

3. **Check cart has items**:
   - Go to cart page
   - Verify items are listed
   - Check total is not £0.00

4. **Check browser console**:
   - F12 → Console tab
   - Look for errors when clicking button

5. **Check Django console**:
   - Look at terminal where server is running
   - Check for error messages

## Most Likely Issue

**90% of the time**: Stripe keys are not configured or are still placeholders.

**Quick fix**:
1. Open `.env` file
2. Replace `sk_test_your_stripe_secret_key_here` with real key
3. Replace `pk_test_your_stripe_publishable_key_here` with real key
4. Restart server: `python manage.py runserver`

## Still Not Working?

If you've checked all the above:
1. Share the error message from browser console (F12)
2. Share any error from Django server console
3. Verify the `.env` file location (should be in project root)
4. Make sure server was restarted after adding keys










