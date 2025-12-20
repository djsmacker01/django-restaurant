# Stripe Payment Setup Guide

This guide will help you set up Stripe payments so the "Proceed to Checkout" button works properly.

## Quick Setup Steps

### 1. Create a Stripe Account

1. Go to [https://stripe.com](https://stripe.com)
2. Click "Sign up" or "Start now"
3. Create your account (it's free to sign up)
4. Complete the account setup

### 2. Get Your Stripe API Keys

1. Log in to your Stripe Dashboard: [https://dashboard.stripe.com](https://dashboard.stripe.com)
2. Make sure you're in **Test Mode** (toggle in the top right - should say "Test mode")
3. Go to **Developers** → **API keys** (or click the "Developers" link in the left sidebar)
4. You'll see two keys:
   - **Publishable key** (starts with `pk_test_`)
   - **Secret key** (starts with `sk_test_`) - Click "Reveal test key" to see it

### 3. Add Keys to Your Environment File

Create or edit your `.env` file in the project root directory:

**Option A: Create `.env` file** (recommended)

Create a file named `.env` in the root directory (`C:\Users\djsma\Desktop\django-restaurant\.env`):

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

**Option B: Use `settings.env` file**

If you prefer to use `settings.env`, add the Stripe keys there:

```env
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

### 4. Example `.env` File

Here's a complete example (replace with your actual keys):

```env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Stripe Test Keys (for development)
STRIPE_SECRET_KEY=sk_test_YOUR_SECRET_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_PUBLISHABLE_KEY_HERE
STRIPE_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET_HERE
```

### 5. Verify Installation

1. Make sure `stripe` is installed:
   ```bash
   pip install stripe
   ```

2. Check if it's in `requirements.txt`:
   ```bash
   cat requirements.txt | grep stripe
   ```
   Should show: `stripe==10.0.0` (or similar version)

3. Restart your Django development server:
   ```bash
   python manage.py runserver
   ```

### 6. Test the Checkout

1. **Add items to cart**: Go to the menu and add items
2. **Go to cart**: Click the cart icon
3. **Click "Proceed to Checkout"**: Should now work!
4. **Use test card**: 
   - Card number: `4242 4242 4242 4242`
   - Expiry: Any future date (e.g., `12/34`)
   - CVC: Any 3 digits (e.g., `123`)
   - ZIP: Any 5 digits (e.g., `12345`)

## Troubleshooting

### Error: "Payment system is not configured"

**Solution**: 
- Check that your `.env` file exists in the project root
- Verify the keys are named correctly: `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY`
- Make sure there are no extra spaces or quotes around the values
- Restart the Django server after adding keys

### Error: "Payment system is not available"

**Solution**:
- Make sure `stripe` package is installed: `pip install stripe`
- Check that `stripe` is imported correctly in `restaurant/views.py`

### Error: "Invalid API Key"

**Solution**:
- Verify you're using **Test Mode** keys (start with `sk_test_` and `pk_test_`)
- Make sure you copied the entire key (they're long!)
- Check for any extra spaces or line breaks in your `.env` file

### Checkout page loads but payment form doesn't appear

**Solution**:
- Open browser console (F12) and check for JavaScript errors
- Verify `stripe_publishable_key` and `client_secret` are being passed to the template
- Make sure you're using the correct publishable key (starts with `pk_test_`)

## Test Cards

Stripe provides test cards for different scenarios:

### Successful Payment
- **Card**: `4242 4242 4242 4242`
- **Expiry**: Any future date
- **CVC**: Any 3 digits

### Card Declined
- **Card**: `4000 0000 0000 0002`
- **Expiry**: Any future date
- **CVC**: Any 3 digits

### Requires Authentication (3D Secure)
- **Card**: `4000 0025 0000 3155`
- **Expiry**: Any future date
- **CVC**: Any 3 digits

### Insufficient Funds
- **Card**: `4000 0000 0000 9995`
- **Expiry**: Any future date
- **CVC**: Any 3 digits

## Production Setup

When you're ready for production:

1. **Switch to Live Mode** in Stripe Dashboard
2. **Get Live API Keys** (starts with `sk_live_` and `pk_live_`)
3. **Update `.env` file** with live keys
4. **Set `DEBUG=False`** in production settings
5. **Never commit** your `.env` file to git (it's in `.gitignore`)

## Security Notes

⚠️ **IMPORTANT**:
- Never commit your `.env` file to version control
- Never share your Secret Key publicly
- Use Test Mode keys for development
- Use Live Mode keys only in production
- The `.env` file is already in `.gitignore` - don't remove it!

## Quick Checklist

- [ ] Created Stripe account
- [ ] Got Test Mode API keys from Stripe Dashboard
- [ ] Created `.env` file in project root
- [ ] Added `STRIPE_SECRET_KEY` to `.env`
- [ ] Added `STRIPE_PUBLISHABLE_KEY` to `.env`
- [ ] Verified `stripe` package is installed
- [ ] Restarted Django server
- [ ] Tested checkout with test card `4242 4242 4242 4242`

## Need Help?

If you're still having issues:

1. Check the Django console for error messages
2. Check browser console (F12) for JavaScript errors
3. Verify your `.env` file is in the correct location
4. Make sure you restarted the server after adding keys
5. Try using the test card `4242 4242 4242 4242` to verify setup

Once you've completed these steps, the "Proceed to Checkout" button should work perfectly! 🎉










