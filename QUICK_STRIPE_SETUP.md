# Quick Stripe Setup - Get Checkout Working in 5 Minutes

## What You Need to Do

The "Proceed to Checkout" button requires Stripe API keys to work. Here's the fastest way to set it up:

### Step 1: Get Stripe Test Keys (2 minutes)

1. Go to: https://dashboard.stripe.com/test/apikeys
2. If you don't have an account, sign up (it's free)
3. Make sure you're in **Test Mode** (toggle in top right)
4. Copy these two keys:
   - **Publishable key** (starts with `pk_test_`)
   - **Secret key** (click "Reveal test key", starts with `sk_test_`)

### Step 2: Add Keys to Your Project (1 minute)

**Option A: Add to `settings.env` file** (Easiest)

Open `settings.env` in your project root and add these lines:

```env
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
```

**Option B: Create `.env` file** (Recommended)

Create a new file named `.env` in the project root with:

```env
SECRET_KEY=django-insecure-^nq^4e4w$+_kbzerrokz!$7sb#4-rxhs_tzx(5obl1%%zt*fwb
DEBUG=True
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
```

### Step 3: Restart Server (30 seconds)

1. Stop your Django server (Ctrl+C)
2. Start it again:
   ```bash
   python manage.py runserver
   ```

### Step 4: Test It! (1 minute)

1. Add items to cart
2. Click "Proceed to Checkout"
3. Use test card: `4242 4242 4242 4242`
   - Expiry: `12/34`
   - CVC: `123`
   - ZIP: `12345`

## That's It! ✅

Your checkout should now work!

## Common Issues

**"Payment system is not configured"**
→ Make sure you added the keys to `settings.env` or `.env` and restarted the server

**Keys not working**
→ Make sure you're using **Test Mode** keys (start with `sk_test_` and `pk_test_`)

**Still not working?**
→ Check the full guide: `STRIPE_SETUP_GUIDE.md`













