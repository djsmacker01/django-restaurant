# Invoice Feature Documentation

## Overview

The invoice feature allows users to download professional PDF invoices for their paid orders. This feature is integrated into the order detail page and provides a complete invoice document with all order information.

## Features

✅ **PDF Invoice Generation**
- Professional invoice layout with restaurant branding
- Complete order details (items, quantities, prices, totals)
- Customer information
- Payment information
- Transaction ID (if available)
- Special instructions (if any)

✅ **Security**
- Only accessible to the order owner
- Only available for paid orders
- Requires user authentication

✅ **User-Friendly**
- Download button appears automatically on order detail page for paid orders
- Clear button with PDF icon
- Instant download when clicked

## How It Works

### For Users

1. **View Order**: Go to "My Orders" and click on any order
2. **Check Payment Status**: Invoice download is only available for orders with "Paid" payment status
3. **Download Invoice**: Click the "Download Invoice" button
4. **PDF Opens**: The invoice PDF will download automatically with filename: `Invoice_{order_number}.pdf`

### Invoice Contents

The PDF invoice includes:

1. **Restaurant Information**
   - Restaurant name (FLAVOUR RESTAURANT)
   - Address, phone, email

2. **Invoice Details**
   - Invoice number (same as order number)
   - Invoice date
   - Order date and time

3. **Customer Information**
   - Customer name
   - Customer email
   - Delivery address (if provided)

4. **Order Items Table**
   - Item name
   - Category
   - Quantity
   - Unit price
   - Subtotal

5. **Payment Information**
   - Payment status
   - Payment method (Stripe)
   - Transaction ID (if available)

6. **Special Instructions** (if any)

7. **Footer**
   - Thank you message
   - Contact information

## Technical Details

### Dependencies

- **reportlab==4.2.5**: PDF generation library
- Already included in `requirements.txt`

### Files Modified/Created

1. **`restaurant/views.py`**
   - Added `order_invoice` view function
   - Generates PDF using reportlab
   - Returns PDF as HTTP response

2. **`restaurant/urls.py`**
   - Added URL pattern: `orders/<int:pk>/invoice/`

3. **`restaurant/templates/restaurant/order_detail.html`**
   - Added "Download Invoice" button (only for paid orders)

4. **`requirements.txt`**
   - Added `reportlab==4.2.5`

### View Function

```python
@login_required
def order_invoice(request, pk):
    """Generate and download invoice PDF for an order."""
    # Security checks
    # PDF generation
    # Return PDF response
```

### URL Pattern

```python
path('orders/<int:pk>/invoice/', views.order_invoice, name='order_invoice'),
```

## Installation

The invoice feature is ready to use! Just make sure reportlab is installed:

```bash
pip install -r requirements.txt
```

## Usage Example

1. User completes a payment
2. Order status changes to "paid"
3. User views order details
4. "Download Invoice" button appears
5. User clicks button
6. PDF invoice downloads automatically

## Invoice Design

- **Color Scheme**: Uses restaurant brand colors (wine red #c41e3a)
- **Layout**: Professional, clean, easy to read
- **Format**: A4 size, portrait orientation
- **Styling**: 
  - Bold headers
  - Clear table layout
  - Professional typography
  - Proper spacing and margins

## Security Features

1. **Authentication Required**: `@login_required` decorator
2. **Owner Verification**: Only order owner can download invoice
3. **Payment Status Check**: Only paid orders can generate invoices
4. **Error Handling**: Redirects with error message if conditions not met

## Future Enhancements (Optional)

- Add restaurant logo to invoice
- Customize restaurant information from settings
- Email invoice automatically after payment
- Add tax breakdown
- Add delivery fee breakdown
- Multiple language support
- Custom invoice templates

## Testing

To test the invoice feature:

1. Create a test order and complete payment
2. Go to order detail page
3. Verify "Download Invoice" button appears
4. Click button
5. Verify PDF downloads correctly
6. Open PDF and verify all information is correct

## Troubleshooting

### Invoice button doesn't appear
- Check that order payment status is "paid"
- Verify user is logged in
- Check that user owns the order

### PDF doesn't download
- Check browser download settings
- Verify reportlab is installed: `pip list | grep reportlab`
- Check Django server logs for errors

### PDF is empty or corrupted
- Check that order has items
- Verify order data is valid
- Check server logs for reportlab errors

## Notes

- Invoice filename format: `Invoice_{order_number}.pdf`
- Invoice uses A4 page size
- All prices formatted to 2 decimal places
- Dates formatted in readable format (e.g., "January 15, 2024")












