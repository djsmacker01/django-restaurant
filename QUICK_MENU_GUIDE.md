# Quick Guide: Adding Menu Items & Images

## 🚀 Quick Start

### For Staff Users (Recommended)

1. **Log in** as a staff user
2. **Click "Add Menu Item"** in the navigation menu (top right, visible only to staff)
3. **Fill the form**:
   - Name: e.g., "Grilled Salmon"
   - Description: e.g., "Fresh Atlantic salmon with herbs"
   - Price: e.g., 24.99
   - Category: Select from dropdown
   - **Image**: Click "Choose File" → Select image
   - Available: ✓ Check this
4. **Click "Create Menu Item"**

### Direct URLs

- **Create**: `http://localhost:8000/restaurant/menu/create/`
- **Menu List**: `http://localhost:8000/restaurant/menu/`
- **Edit**: `http://localhost:8000/restaurant/menu/{id}/update/`

---

## 📸 Adding Images

### Step-by-Step

1. **Prepare Your Image**
   - Format: JPG, PNG, or GIF
   - Size: 800x600px or larger (recommended)
   - File size: Under 2MB

2. **Upload Image**
   - In the menu item form, find "Image" field
   - Click "Choose File" button
   - Select your image file
   - Image preview will appear (if supported by browser)

3. **Save**
   - Click "Create Menu Item" or "Update Menu Item"
   - Image is automatically saved to `media/menu_images/`

### Image Tips

✅ **Do:**
- Use high-quality food photos
- Keep images well-lit and clear
- Use consistent image sizes
- Optimize images before uploading

❌ **Don't:**
- Upload very large files (>5MB)
- Use unsupported formats (use JPG/PNG/GIF)
- Upload blurry or dark images

---

## 🔑 Staff User Access

### Check if You're Staff

1. Log in to your account
2. Look for "Add Menu Item" link in navigation
3. If you see it → You're a staff user ✅
4. If you don't see it → You need staff permissions ❌

### Make a User Staff (Admin Only)

**Via Django Admin:**
1. Go to: `http://localhost:8000/admin/`
2. Navigate to: Users → Select user
3. Check "Staff status" checkbox
4. Save

**Via Django Shell:**
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
user = User.objects.get(username='your_username')
user.is_staff = True
user.save()
```

---

## 📋 Menu Item Fields Explained

| Field | Required | Example | Notes |
|-------|----------|---------|-------|
| **Name** | ✅ Yes | "Grilled Salmon" | Menu item title |
| **Description** | ❌ No | "Fresh Atlantic salmon..." | Detailed description |
| **Price** | ✅ Yes | 24.99 | Price in £ (must be > 0) |
| **Category** | ✅ Yes | Main Course | Appetizer/Main/Dessert/Drink |
| **Image** | ❌ No | salmon.jpg | Upload food photo |
| **Available** | ✅ Yes | ✓ Checked | Show on menu? |

---

## 🎯 Common Tasks

### Add a New Menu Item
```
1. Log in as staff
2. Click "Add Menu Item" (navigation)
3. Fill form + upload image
4. Click "Create Menu Item"
```

### Edit Existing Menu Item
```
1. Go to menu list
2. Click on menu item
3. Go to: /restaurant/menu/{id}/update/
4. Make changes
5. Click "Update Menu Item"
```

### Add Image to Existing Item
```
1. Edit the menu item
2. Scroll to "Image" field
3. Click "Choose File"
4. Select image
5. Save
```

### Delete Menu Item
```
1. Go to menu item detail page
2. Click "Delete" button
3. Confirm deletion
```

---

## 🛠️ Troubleshooting

### "Add Menu Item" Link Not Showing
- **Solution**: You need staff permissions
- Ask admin to make you staff user

### Image Not Uploading
- **Check**: File format (JPG/PNG/GIF only)
- **Check**: File size (should be < 5MB)
- **Check**: `media/` directory exists

### Image Not Displaying
- **Check**: Image was saved correctly
- **Check**: File path: `media/menu_images/`
- **Check**: Django server is running
- **Check**: MEDIA_URL in settings.py

### Form Errors
- **Check**: All required fields filled
- **Check**: Price is greater than 0
- **Check**: Name is not empty

---

## 📁 Where Images Are Stored

- **Location**: `media/menu_images/`
- **URL**: `http://localhost:8000/media/menu_images/filename.jpg`
- **Auto-created**: Django creates directory automatically

---

## 💡 Pro Tips

1. **Batch Upload**: Use Django Admin for adding multiple items quickly
2. **Image Optimization**: Compress images before uploading (use tools like TinyPNG)
3. **Consistent Naming**: Use descriptive filenames (e.g., `grilled-salmon.jpg`)
4. **Test First**: Add one item, check it displays correctly, then add more
5. **Backup**: Keep original images in a separate folder

---

## 📚 More Information

- **Full Guide**: See `HOW_TO_ADD_MENU_ITEMS.md`
- **Data Management**: See `DATA_AND_CONTENT_GUIDE.md`
- **Sample Data**: Run `python manage.py create_sample_data`

---

## 🎬 Example Workflow

**Adding "Chocolate Lava Cake":**

1. ✅ Log in as staff
2. ✅ Click "Add Menu Item"
3. ✅ Fill form:
   - Name: `Chocolate Lava Cake`
   - Description: `Warm chocolate cake with molten center, served with vanilla ice cream`
   - Price: `9.99`
   - Category: `Dessert`
   - Image: Upload `chocolate-lava-cake.jpg`
   - Available: ✓
4. ✅ Click "Create Menu Item"
5. ✅ Done! Item appears on menu immediately

---

**Need Help?** Check the full guide: `HOW_TO_ADD_MENU_ITEMS.md`

