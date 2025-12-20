# Production Content Management Guide

This guide explains how to manage menu items, prices, and content when your restaurant platform is live in production.

## 🎯 Overview

When your site is live, you need a way to:
- ✅ Add new menu items
- ✅ Update prices
- ✅ Upload images
- ✅ Manage availability
- ✅ Update descriptions
- ✅ All without affecting users or taking the site down

## 🔐 Access Methods for Production

### Method 1: Django Admin Panel (Recommended)

**Best for**: Daily content management, bulk updates, non-technical staff

#### Setup

1. **Ensure Admin is Enabled** (already configured)
   - Admin is available at: `https://yourdomain.com/admin/`
   - Requires superuser or staff account

2. **Create Admin Account** (if not exists)
   ```bash
   python manage.py createsuperuser
   ```
   - Username: your_admin_username
   - Email: admin@yourrestaurant.com
   - Password: (choose strong password)

3. **Access Admin Panel**
   - Go to: `https://yourdomain.com/admin/`
   - Log in with superuser credentials
   - Navigate to: **RESTAURANT** → **Menu Items**

#### Features Available

- ✅ **List View**: See all menu items at once
- ✅ **Search**: Search by name or description
- ✅ **Filter**: Filter by category, availability, date
- ✅ **Bulk Actions**: Select multiple items and update
- ✅ **Quick Edit**: Edit items directly from list
- ✅ **Image Upload**: Upload images through admin interface
- ✅ **Date Management**: See created/updated dates

### Method 2: Staff Form Interface

**Best for**: Staff members who need simpler interface

#### Setup

1. **Create Staff Users**
   - Go to Admin → Users
   - Create user or edit existing
   - Check "Staff status" ✅
   - Save

2. **Access Staff Interface**
   - Staff users can log in at: `https://yourdomain.com/accounts/login/`
   - After login, they'll see "Add Menu Item" in navigation
   - Can create/edit menu items through web interface

### Method 3: Django Shell (Advanced)

**Best for**: Bulk updates, automated scripts, technical users

```bash
# SSH into your production server
python manage.py shell
```

```python
from restaurant.models import MenuItem
from decimal import Decimal

# Update price for specific item
item = MenuItem.objects.get(name="Grilled Salmon")
item.price = Decimal('26.99')  # New price
item.save()

# Bulk update prices (e.g., 10% increase)
items = MenuItem.objects.filter(category='main')
for item in items:
    item.price = item.price * Decimal('1.10')
    item.save()
```

---

## 📝 Common Production Tasks

### 1. Adding a New Menu Item

**Via Admin:**
1. Go to: `https://yourdomain.com/admin/restaurant/menuitem/`
2. Click "Add Menu Item" (top right)
3. Fill form:
   - Name: "New Dish Name"
   - Description: "Description here"
   - Price: 24.99
   - Category: Select from dropdown
   - **Image**: Click "Choose File" → Upload image
   - Available: ✓ Check to show on menu
4. Click "Save"
5. **Result**: Item appears on menu immediately! ✅

**Via Staff Interface:**
1. Log in as staff user
2. Click "Add Menu Item" in navigation
3. Fill form and save

### 2. Updating Prices

**Single Item:**
1. Admin → Menu Items → Click item name
2. Change "Price" field
3. Click "Save"
4. **Result**: New price shows immediately on website ✅

**Bulk Price Update:**
1. Admin → Menu Items
2. Select multiple items (checkboxes)
3. Select action: "Change price" (if custom action exists)
   OR
4. Use Django shell for bulk updates (see Method 3 above)

**Price Update Workflow:**
```
1. Log in to admin
2. Go to Menu Items
3. Click on item to edit
4. Update price field
5. Save
6. Verify on website (menu page)
```

### 3. Uploading Images

**Via Admin:**
1. Edit menu item
2. Scroll to "Image" field
3. Click "Choose File"
4. Select image (JPG/PNG/GIF)
5. Click "Save"
6. Image appears on website immediately

**Image Requirements:**
- Format: JPG, PNG, GIF
- Size: Recommended 800x600px or larger
- File size: Under 2MB (for fast loading)
- Storage: Automatically saved to `media/menu_images/`

### 4. Managing Availability

**Make Item Unavailable (Temporarily):**
1. Admin → Menu Items → Edit item
2. Uncheck "Available" checkbox
3. Save
4. **Result**: Item disappears from public menu ✅

**Make Item Available:**
1. Edit item
2. Check "Available" checkbox
3. Save
4. **Result**: Item appears on menu ✅

**Bulk Availability:**
1. Select multiple items
2. Use bulk action to change availability

### 5. Updating Descriptions

1. Admin → Menu Items → Edit item
2. Update "Description" field
3. Save
4. Changes appear immediately

### 6. Date Management

**View Creation/Update Dates:**
- Admin shows "Created at" and "Updated at" automatically
- Useful for tracking when items were added/modified

**Note**: Dates are automatically managed by Django

---

## 🔄 Production Workflow Examples

### Daily Menu Update

**Scenario**: Update prices for daily specials

```
1. Log in to admin (https://yourdomain.com/admin/)
2. Go to Menu Items
3. Filter by category (e.g., "Main Course")
4. Edit each special item
5. Update price
6. Save
7. Verify on website
```

### Adding Weekly Special

**Scenario**: Add new weekly special menu item

```
1. Log in to admin
2. Click "Add Menu Item"
3. Fill form:
   - Name: "Weekly Special: Pasta"
   - Description: "This week's special pasta dish"
   - Price: 18.99
   - Category: Main Course
   - Image: Upload pasta.jpg
   - Available: ✓
4. Save
5. Item appears on menu immediately
```

### Seasonal Menu Update

**Scenario**: Update menu for new season

```
1. Log in to admin
2. Review all menu items
3. Update seasonal items:
   - Change descriptions
   - Update prices if needed
   - Upload new seasonal images
4. Make seasonal items available
5. Make out-of-season items unavailable
6. Save changes
```

---

## 🛡️ Best Practices for Production

### 1. **Backup Before Major Changes**
```bash
# Backup database before bulk updates
python manage.py dumpdata restaurant > backup.json
```

### 2. **Test Changes First**
- Make changes in admin
- Verify on website immediately
- Check mobile view too

### 3. **Use Descriptive Names**
- Clear, consistent naming
- Easy to find in admin list

### 4. **Image Optimization**
- Compress images before uploading
- Use consistent dimensions
- Optimize for web (under 2MB)

### 5. **Price Updates**
- Update prices during low-traffic hours (optional)
- Verify prices after update
- Consider bulk update scripts for large changes

### 6. **Availability Management**
- Use "Available" checkbox to hide items (don't delete)
- Easier to restore later
- Maintains order history

### 7. **Regular Reviews**
- Review menu weekly/monthly
- Update outdated descriptions
- Refresh images seasonally

---

## 🔒 Security Considerations

### Admin Access Security

1. **Strong Passwords**
   - Use complex passwords for admin accounts
   - Enable 2FA if available (Django extensions)

2. **Staff Permissions**
   - Only grant staff status to trusted users
   - Regular users can't access admin

3. **HTTPS Required**
   - Admin should only be accessible via HTTPS
   - Already configured in production settings

4. **IP Restrictions** (Optional)
   - Restrict admin access to specific IPs
   - Use Django middleware or web server config

### Content Validation

- Prices must be > 0 (enforced by form)
- Required fields validated
- Image formats restricted (JPG/PNG/GIF)

---

## 📊 Monitoring & Tracking

### View Recent Changes

1. **Admin List View**
   - Shows "Created at" and "Updated at" columns
   - Sort by date to see recent changes

2. **Django Logs**
   - Check server logs for admin actions
   - Useful for audit trail

### Analytics (Optional)

- Track which items are popular
- Monitor price change impact
- Use order data to inform menu decisions

---

## 🚀 Quick Reference

### Admin URLs

- **Admin Login**: `https://yourdomain.com/admin/`
- **Menu Items**: `https://yourdomain.com/admin/restaurant/menuitem/`
- **Add Item**: `https://yourdomain.com/admin/restaurant/menuitem/add/`

### Staff URLs

- **Login**: `https://yourdomain.com/accounts/login/`
- **Create Menu Item**: `https://yourdomain.com/restaurant/menu/create/`
- **Menu List**: `https://yourdomain.com/restaurant/menu/`

### Common Commands

```bash
# Create superuser
python manage.py createsuperuser

# Create staff user (via shell)
python manage.py shell
# Then: user.is_staff = True; user.save()

# Backup data
python manage.py dumpdata restaurant > backup.json

# Load data
python manage.py loaddata backup.json
```

---

## 📱 Mobile Admin Access

### Using Admin on Mobile

- Admin interface is responsive
- Can manage content from phone/tablet
- Useful for quick updates on-the-go

### Mobile Workflow

1. Log in to admin on mobile browser
2. Navigate to Menu Items
3. Edit items as needed
4. Upload images from phone gallery
5. Save changes

---

## 🔧 Troubleshooting Production Issues

### Images Not Uploading

**Check:**
1. File permissions on `media/` directory
2. Disk space on server
3. File size limits in settings
4. Web server configuration (Nginx/Apache)

**Solution:**
```bash
# Check permissions
chmod -R 755 media/
chown -R www-data:www-data media/

# Check disk space
df -h
```

### Changes Not Appearing

**Check:**
1. Browser cache (hard refresh: Ctrl+F5)
2. CDN cache (if using CDN)
3. Server restart needed (rare)
4. Database connection

**Solution:**
- Clear browser cache
- Wait a few minutes for CDN to update
- Check server logs

### Admin Not Accessible

**Check:**
1. HTTPS configuration
2. Firewall rules
3. Server status
4. URL configuration

---

## 📋 Production Checklist

Before going live, ensure:

- ✅ Admin account created
- ✅ Staff users created (if needed)
- ✅ Media directory configured
- ✅ Image uploads working
- ✅ HTTPS enabled for admin
- ✅ Backup system in place
- ✅ Staff trained on admin interface
- ✅ Test content management workflow

---

## 🎓 Training Staff

### For Non-Technical Staff

1. **Create Staff Account** for them
2. **Show Admin Interface**:
   - How to log in
   - How to find menu items
   - How to edit prices
   - How to upload images
3. **Practice Session**: Let them try with test items
4. **Documentation**: Share this guide

### Quick Training Steps

```
1. Log in to admin
2. Find "Menu Items" section
3. Click on item to edit
4. Make changes
5. Click "Save"
6. Verify on website
```

---

## 💡 Pro Tips

1. **Bookmark Admin URL**: Save admin login page
2. **Use Search**: Admin has powerful search functionality
3. **Bulk Actions**: Select multiple items for bulk updates
4. **Preview Changes**: Check website after each change
5. **Regular Backups**: Backup database regularly
6. **Image Library**: Keep organized image library
7. **Price History**: Document price changes (optional)

---

## 📞 Support

If you need help:
1. Check Django server logs
2. Check web server logs (Nginx/Apache)
3. Verify database connection
4. Check file permissions
5. Review this guide

---

## 🎯 Summary

**For Daily Content Management:**
- Use Django Admin (`/admin/`) - Easiest and most powerful
- Create staff users for team members
- All changes appear immediately on website
- No code changes needed
- No downtime required

**Key Points:**
- ✅ Admin is always available at `/admin/`
- ✅ Changes are instant (no deployment needed)
- ✅ Images upload automatically
- ✅ Prices update immediately
- ✅ Availability can be toggled easily
- ✅ Safe and secure (requires login)

**Your workflow:**
1. Log in to admin
2. Edit menu items
3. Save
4. Done! ✅









