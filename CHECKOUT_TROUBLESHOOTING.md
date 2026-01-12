# Checkout Button Not Working - Troubleshooting Guide

## Your Stripe Keys Are Configured ✅

I can see your Stripe keys are set in `.env`. The issue might be:

## Step-by-Step Debugging

### 1. Restart Django Server

**IMPORTANT**: After adding/updating `.env` file, you MUST restart the server!

```bash
# Stop the server (Ctrl+C in the terminal)
# Then restart:
source venv/Scripts/activate
python manage.py runserver
```

### 2. Check If You're Logged In

- Look at the top right of the page
- Do you see your username or "Login" button?
- **If you see "Login"**: Click it and log in first
- Checkout requires you to be logged in

### 3. Check If Cart Has Items

- Go to the cart page
- Do you see items listed?
- Is the total greater than £0.00?
- **If cart is empty**: Add items from the menu first

### 4. Check Browser Console for Errors

1. Open your browser
2. Press **F12** (or Right-click → Inspect)
3. Click the **Console** tab
4. Click "Proceed to Checkout" button
5. Look for any **red error messages**

**Common errors to look for**:
- `Stripe is not defined`
- `Invalid API key`
- `CORS error`
- `404 Not Found`
- `500 Internal Server Error`

### 5. Check Django Server Console

Look at the terminal where `python manage.py runserver` is running:

**What to check**:
- Any error messages when you click checkout?
- Messages like "Payment system is not configured"?
- Any traceback/error output?

### 6. Test the URL Directly

Try visiting this URL directly in your browser:
```
http://127.0.0.1:8000/restaurant/checkout/
```

**What happens**:
- ✅ **If it works**: The button link might have an issue
- ❌ **If it redirects to cart**: Check the error message at the top
- ❌ **If it redirects to login**: You need to log in first
- ❌ **If 404 error**: URL routing issue

### 7. Check for Error Messages on Page

After clicking "Proceed to Checkout", check the top of the page for:
- Red error messages (alerts)
- Yellow warning messages
- Any Django messages

**Common messages**:
- "Payment system is not configured"
- "Your cart is empty"
- "Payment system is not available"

## Quick Fixes

### Fix 1: Restart Server
```bash
# Stop server (Ctrl+C)
source venv/Scripts/activate
python manage.py runserver
```

### Fix 2: Clear Browser Cache
- Press **Ctrl+Shift+Delete**
- Clear cache and cookies
- Refresh the page

### Fix 3: Check Login Status
- Make sure you're logged in
- Username should appear in top right

### Fix 4: Verify Cart Has Items
- Add items to cart
- Check cart page shows items
- Total should be > £0.00

## What to Share If Still Not Working

If none of the above works, please share:

1. **Browser Console Errors** (F12 → Console tab)
2. **Django Server Errors** (from terminal)
3. **What happens when you click the button**:
   - Does the page reload?
   - Does nothing happen at all?
   - Do you see an error message?
   - Does it redirect somewhere?

4. **Are you logged in?** (Yes/No)
5. **Does cart have items?** (Yes/No)
6. **What URL shows in browser** when you click checkout?

## Most Common Issue

**90% of cases**: Server wasn't restarted after adding Stripe keys.

**Solution**: Restart the Django server!













