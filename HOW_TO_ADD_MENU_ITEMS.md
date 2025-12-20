# How to Add Menu Items and Images

This guide explains how to add new menu items and upload images to your restaurant menu.

## Methods to Add Menu Items

There are **3 ways** to add menu items:

1. **Via Staff Form** (Recommended for staff users)
2. **Via Django Admin** (For administrators)
3. **Via Management Command** (For bulk creation)

---

## Method 1: Via Staff Form (Recommended)

### Prerequisites
- You must be logged in as a **staff user**
- Staff users have special permissions to create/edit menu items

### Steps

1. **Log in as Staff User**
   - Go to: `http://localhost:8000/accounts/login/`
   - Log in with a staff account

2. **Navigate to Create Menu Item**
   - Option A: Go directly to: `http://localhost:8000/restaurant/menu/create/`
   - Option B: Look for "Create Menu Item" link in navigation (if available)

3. **Fill Out the Form**
   - **Name**: Enter the menu item name (e.g., "Grilled Salmon")
   - **Description**: Add a description (optional but recommended)
   - **Price**: Enter price in £ (e.g., 24.99)
   - **Category**: Select from:
     - Appetizer
     - Main Course
     - Dessert
     - Drink
   - **Image**: Click "Choose File" and select an image
   - **Available**: Check this box to make item visible on menu

4. **Upload Image**
   - Click the "Choose File" button
   - Select an image file (JPG, PNG, GIF)
   - Recommended size: 800x600px or larger
   - Image will be stored in `media/menu_images/`

5. **Save**
   - Click "Create Menu Item" button
   - You'll be redirected to the menu item detail page

### Editing Existing Menu Items

1. **Find the Menu Item**
   - Go to menu list: `http://localhost:8000/restaurant/menu/`
   - Click on the menu item you want to edit

2. **Edit Menu Item**
   - Go to: `http://localhost:8000/restaurant/menu/{id}/update/`
   - Or look for "Edit" button on the menu item detail page

3. **Update Information**
   - Change any fields you want
   - To change image: Click "Choose File" and select new image
   - Click "Update Menu Item" to save

---

## Method 2: Via Django Admin

### Prerequisites
- You must be logged in as a **superuser** (admin)
- Superusers have full access to Django admin

### Steps

1. **Access Admin Panel**
   - Go to: `http://localhost:8000/admin/`
   - Log in with superuser credentials

2. **Navigate to Menu Items**
   - Click on "Menu Items" under "RESTAURANT" section
   - Or go directly to: `http://localhost:8000/admin/restaurant/menuitem/`

3. **Add New Menu Item**
   - Click "Add Menu Item" button (top right)
   - Fill out all fields:
     - Name
     - Description
     - Price
     - Category
     - Image (upload file)
     - Available (checkbox)
   - Click "Save"

4. **Edit Existing Menu Item**
   - Click on the menu item name in the list
   - Make changes
   - Click "Save"

### Admin Features

- **Bulk Actions**: Select multiple items and perform actions
- **Filtering**: Filter by category, availability, date
- **Search**: Search by name or description
- **List View**: See all menu items at once

---

## Method 3: Via Management Command (Bulk Creation)

### For Creating Sample Data

```bash
# Activate virtual environment
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # Linux/Mac

# Create sample menu items
python manage.py create_sample_data
```

This creates 25 sample menu items across all categories.

### For Custom Bulk Creation

You can modify `restaurant/management/commands/create_sample_data.py` to add your own menu items.

---

## Image Requirements and Tips

### Supported Formats
- **JPG/JPEG** (recommended)
- **PNG** (good for transparency)
- **GIF** (for animated images, though static is recommended)

### Recommended Image Specifications
- **Size**: 800x600px or larger
- **Aspect Ratio**: 4:3 or 16:9
- **File Size**: Under 2MB (for faster loading)
- **Format**: JPG for photos, PNG for graphics

### Image Storage
- Images are stored in: `media/menu_images/`
- Django automatically creates this directory when first image is uploaded
- Images are accessible at: `http://localhost:8000/media/menu_images/filename.jpg`

### Image Best Practices
1. **Use High-Quality Images**: Clear, well-lit food photos work best
2. **Consistent Sizing**: Try to use similar dimensions for all menu items
3. **Optimize Images**: Compress images before uploading to reduce file size
4. **Descriptive Filenames**: Use descriptive names (e.g., `grilled-salmon.jpg`)

---

## Creating a Staff User

If you don't have a staff user account:

### Option 1: Via Django Admin (Superuser)

1. Create a superuser (if you don't have one):
   ```bash
   python manage.py createsuperuser
   ```

2. Log in to admin: `http://localhost:8000/admin/`

3. Go to Users section

4. Create a new user or edit existing user

5. Check "Staff status" checkbox

6. Save

### Option 2: Via Django Shell

```bash
python manage.py shell
```

Then in Python shell:
```python
from django.contrib.auth.models import User

# Create staff user
user = User.objects.create_user(
    username='staff_user',
    email='staff@example.com',
    password='your_password'
)
user.is_staff = True
user.save()
```

---

## Quick Reference

### URLs for Menu Management

- **Menu List**: `/restaurant/menu/`
- **Create Menu Item**: `/restaurant/menu/create/` (staff only)
- **Edit Menu Item**: `/restaurant/menu/{id}/update/` (staff only)
- **Delete Menu Item**: `/restaurant/menu/{id}/delete/` (staff only)
- **Menu Item Detail**: `/restaurant/menu/{id}/`

### Menu Item Fields

| Field | Required | Description |
|-------|----------|-------------|
| Name | Yes | Menu item name |
| Description | No | Item description |
| Price | Yes | Price in £ (must be > 0) |
| Category | Yes | Appetizer, Main Course, Dessert, or Drink |
| Image | No | Upload image file |
| Available | Yes | Checkbox to show/hide item |

---

## Troubleshooting

### Image Not Uploading

1. **Check File Permissions**
   - Ensure `media/` directory exists and is writable
   - Django creates it automatically, but check if it exists

2. **Check File Size**
   - Large files (>5MB) may fail
   - Compress images before uploading

3. **Check File Format**
   - Only JPG, PNG, GIF are supported
   - Convert other formats first

4. **Check Pillow Installation**
   ```bash
   pip install pillow
   ```

### Menu Item Not Appearing

1. **Check "Available" Checkbox**
   - Menu items with "Available" unchecked won't show on menu

2. **Check User Permissions**
   - Only staff users can create/edit menu items
   - Regular users can only view menu items

3. **Clear Browser Cache**
   - Sometimes old data is cached
   - Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)

### Form Not Saving

1. **Check Required Fields**
   - Name and Price are required
   - Ensure price is greater than 0

2. **Check Form Validation**
   - Look for error messages on the form
   - Fix any validation errors

3. **Check Server Logs**
   - Look at Django server terminal for error messages

---

## Example: Adding a New Menu Item

Let's add "Chocolate Cake" as a dessert:

1. **Log in** as staff user
2. **Go to**: `http://localhost:8000/restaurant/menu/create/`
3. **Fill form**:
   - Name: `Chocolate Cake`
   - Description: `Rich chocolate cake with chocolate frosting`
   - Price: `8.99`
   - Category: `Dessert`
   - Image: Upload `chocolate-cake.jpg`
   - Available: ✓ (checked)
4. **Click**: "Create Menu Item"
5. **Result**: Menu item created and visible on menu!

---

## Need Help?

- Check Django server logs for errors
- Verify user has staff permissions
- Ensure media directory exists
- Check image file format and size

For more information, see:
- `DATA_AND_CONTENT_GUIDE.md` - Detailed data management guide
- `TESTING_GUIDE.md` - Testing procedures









