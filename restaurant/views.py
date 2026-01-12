from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlparse, parse_qs
import uuid
from decimal import Decimal
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

try:
    import stripe
    stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
except ImportError:
    stripe = None

from .models import MenuItem, Order, OrderItem, Reservation
from .forms import MenuItemForm, ReservationForm, OrderItemForm


def is_staff_user(user):
    """Check if user is staff."""
    return user.is_staff


def home(request):
    """Home page view."""
    featured_items = MenuItem.objects.filter(is_available=True)[:6]
    
    context = {
        'featured_items': featured_items,
    }
    return render(request, 'restaurant/home.html', context)


def menu_list(request):
    """
    View function for displaying the menu list.
    Includes filtering and search functionality.
    """
    menu_items = MenuItem.objects.filter(is_available=True)
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    if category_filter:
        menu_items = menu_items.filter(category=category_filter)
    
    if search_query:
        menu_items = menu_items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    categories = {}
    for item in menu_items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)
    
    context = {
        'menu_items': menu_items,
        'categories': categories,
        'category_filter': category_filter,
        'search_query': search_query,
        'category_choices': MenuItem.CATEGORY_CHOICES,
    }
    return render(request, 'restaurant/menu_list.html', context)


def menu_detail(request, pk):
    """View for displaying menu item details."""
    menu_item = get_object_or_404(MenuItem, pk=pk)
    context = {
        'menu_item': menu_item,
    }
    return render(request, 'restaurant/menu_detail.html', context)


@login_required
@user_passes_test(is_staff_user)
def menu_item_create(request):
    """View for creating a new menu item (staff only)."""
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save()
            messages.success(request, f'Menu item "{menu_item.name}" created successfully!')
            return redirect('restaurant:menu_detail', pk=menu_item.pk)
    else:
        form = MenuItemForm()
    
    context = {
        'form': form,
        'title': 'Create Menu Item',
    }
    return render(request, 'restaurant/menu_item_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def menu_item_update(request, pk):
    """View for updating a menu item (staff only)."""
    menu_item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Menu item "{menu_item.name}" updated successfully!')
            return redirect('restaurant:menu_detail', pk=menu_item.pk)
    else:
        form = MenuItemForm(instance=menu_item)
    
    context = {
        'form': form,
        'menu_item': menu_item,
        'title': 'Update Menu Item',
    }
    return render(request, 'restaurant/menu_item_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def menu_item_delete(request, pk):
    """View for deleting a menu item (staff only)."""
    menu_item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == 'POST':
        menu_item_name = menu_item.name
        menu_item.delete()
        messages.success(request, f'Menu item "{menu_item_name}" deleted successfully!')
        return redirect('restaurant:menu_list')
    
    context = {
        'menu_item': menu_item,
    }
    return render(request, 'restaurant/menu_item_confirm_delete.html', context)


@login_required
def add_to_cart(request):
    """Add item to shopping cart."""
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            menu_item_id = form.cleaned_data['menu_item_id']
            quantity = form.cleaned_data['quantity']
            
            try:
                menu_item = MenuItem.objects.get(pk=menu_item_id, is_available=True)
            except MenuItem.DoesNotExist:
                messages.error(request, 'Menu item not found or unavailable.')
                return redirect('restaurant:menu_list')
            
            cart, created = Order.objects.get_or_create(
                user=request.user,
                status='pending',
                payment_status='pending',
                defaults={'order_number': f'CART-{uuid.uuid4().hex[:8].upper()}'}
            )
            
            order_item, created = OrderItem.objects.get_or_create(
                order=cart,
                menu_item=menu_item,
                defaults={'quantity': quantity, 'price': menu_item.price}
            )
            
            if not created:
                order_item.quantity += quantity
                order_item.save()
            
            cart.calculate_total()
            messages.success(request, f'✓ Added {quantity}x {menu_item.name} to cart! Continue shopping or view your cart.')
            
            referer = request.META.get('HTTP_REFERER', '')
            if referer and ('menu' in referer or 'restaurant/menu' in referer):
                parsed = urlparse(referer)
                query_params = parse_qs(parsed.query)
                url = reverse('restaurant:menu_list')
                if query_params:
                    params = '&'.join([f"{k}={v[0]}" for k, v in query_params.items()])
                    url = f"{url}?{params}"
                return redirect(url)
            return redirect('restaurant:menu_list')
        else:
            messages.error(request, 'Invalid form data.')
    
    return redirect('restaurant:menu_list')


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
    
    context = {
        'cart': cart,
        'order_items': order_items,
    }
    return render(request, 'restaurant/cart.html', context)


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update quantity of cart item."""
    order_item = get_object_or_404(OrderItem, pk=item_id, order__user=request.user)
    cart = order_item.order
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        order_item.quantity = quantity
        order_item.save()
        messages.success(request, 'Cart updated!')
    else:
        order_item.delete()
        messages.success(request, 'Item removed from cart!')
    
    cart.calculate_total()
    
    return redirect('restaurant:cart')


@login_required
@require_POST
def remove_cart_item(request, item_id):
    """Remove item from cart."""
    order_item = get_object_or_404(OrderItem, pk=item_id, order__user=request.user)
    cart = order_item.order
    order_item.delete()
    
    cart.calculate_total()
    
    messages.success(request, 'Item removed from cart!')
    return redirect('restaurant:cart')


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
    
    total_amount = cart.calculate_total()
    
    if not stripe:
        messages.error(request, 'Payment system is not available. Please contact support.')
        return redirect('restaurant:cart')
    
    stripe_secret_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
    stripe_publishable_key = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
    
    if not stripe_secret_key or not stripe_publishable_key:
        messages.error(request, 'Payment system is not configured. Please contact support.')
        return redirect('restaurant:cart')
    
    try:
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


@login_required
def payment_cancel(request):
    """Handle cancelled payment."""
    messages.info(request, 'Payment was cancelled. Your items are still in your cart.')
    return render(request, 'restaurant/payment_cancel.html')


@login_required
def order_list(request):
    """View user's orders."""
    orders = Order.objects.filter(user=request.user).exclude(status='pending', payment_status='pending')
    orders = orders.order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'restaurant/order_list.html', context)


@login_required
def order_detail(request, pk):
    """View order details."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    order_items = order.order_items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'restaurant/order_detail.html', context)


@login_required
def order_invoice(request, pk):
    """Generate and download invoice PDF for an order."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    
    if order.payment_status != 'paid':
        messages.error(request, 'Invoice is only available for paid orders.')
        return redirect('restaurant:order_detail', pk=pk)
    
    order_items = order.order_items.all()
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#c41e3a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    
    restaurant_info = [
        [Paragraph('<b>FLAVOUR RESTAURANT</b>', title_style)],
        [Paragraph('32 Chepstow', normal_style)],
        [Paragraph('Newport', normal_style)],
        [Paragraph('Phone: +44 20 1234 5678', normal_style)],
        [Paragraph('Email: info@flavourrestaurant.com', normal_style)],
    ]
    
    restaurant_table = Table(restaurant_info, colWidths=[7*inch])
    restaurant_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(restaurant_table)
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph('INVOICE', heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    customer_name = order.user.get_full_name() if order.user.get_full_name() else order.user.username
    
    info_data = [
        ['Invoice Number:', order.order_number],
        ['Invoice Date:', order.created_at.strftime('%B %d, %Y')],
        ['Order Date:', order.created_at.strftime('%B %d, %Y at %I:%M %p')],
        ['Customer Name:', customer_name],
        ['Customer Email:', order.user.email or 'N/A'],
    ]
    
    if order.delivery_address:
        info_data.append(['Delivery Address:', order.delivery_address])
    
    info_table = Table(info_data, colWidths=[2*inch, 5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a1a1a')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph('Order Items', heading_style))
    
    table_data = [['Item', 'Category', 'Quantity', 'Unit Price', 'Subtotal']]
    
    for item in order_items:
        table_data.append([
            item.menu_item.name,
            item.menu_item.get_category_display(),
            str(item.quantity),
            f'£{item.price:.2f}',
            f'£{item.subtotal:.2f}'
        ])
    
    table_data.append([
        '',
        '',
        '',
        Paragraph('<b>Total:</b>', normal_style),
        Paragraph(f'<b>£{order.total_amount:.2f}</b>', normal_style)
    ])
    
    items_table = Table(table_data, colWidths=[2.5*inch, 1.5*inch, 0.8*inch, 1.2*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c41e3a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -2), colors.HexColor('#1a1a1a')),
        ('ALIGN', (0, 1), (-1, -2), 'LEFT'),
        ('ALIGN', (2, 1), (2, -2), 'CENTER'),
        ('ALIGN', (3, 1), (4, -2), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -2), 8),
        ('TOPPADDING', (0, 1), (-1, -2), 8),
        ('GRID', (0, 0), (-1, -2), 0.5, colors.HexColor('#dee2e6')),
        
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#1a1a1a')),
        ('ALIGN', (0, -1), (2, -1), 'RIGHT'),
        ('ALIGN', (3, -1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        ('TOPPADDING', (0, -1), (-1, -1), 12),
        ('LINEABOVE', (3, -1), (-1, -1), 1, colors.HexColor('#c41e3a')),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 0.3*inch))
    
    payment_info = [
        [Paragraph('<b>Payment Information</b>', heading_style)],
        [Paragraph(f'Payment Status: <b>{order.get_payment_status_display()}</b>', normal_style)],
        [Paragraph(f'Payment Method: Stripe', normal_style)],
    ]
    
    if order.stripe_payment_intent_id:
        payment_info.append([Paragraph(f'Transaction ID: {order.stripe_payment_intent_id}', normal_style)])
    
    payment_table = Table(payment_info, colWidths=[7*inch])
    payment_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(payment_table)
    elements.append(Spacer(1, 0.3*inch))
    
    if order.special_instructions:
        instructions = [
            [Paragraph('<b>Special Instructions</b>', heading_style)],
            [Paragraph(order.special_instructions, normal_style)],
        ]
        instructions_table = Table(instructions, colWidths=[7*inch])
        instructions_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(instructions_table)
        elements.append(Spacer(1, 0.3*inch))
    
    footer_text = Paragraph(
        '<i>Thank you for your order! We appreciate your business.</i><br/>'
        '<i>For any inquiries, please contact us at info@flavourrestaurant.com</i>',
        ParagraphStyle(
            'Footer',
            parent=normal_style,
            fontSize=9,
            textColor=colors.HexColor('#6c757d'),
            alignment=TA_CENTER,
            spaceBefore=20
        )
    )
    elements.append(footer_text)
    
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{order.order_number}.pdf"'
    
    return response


@login_required
def reservation_create(request):
    """View for creating a reservation."""
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.email = request.user.email
            reservation.status = 'pending'
            reservation.save()
            messages.success(request, 'Reservation created successfully! We will confirm it shortly.')
            return redirect('restaurant:reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm()
    
    context = {
        'form': form,
        'title': 'Make a Reservation',
    }
    return render(request, 'restaurant/reservation_form.html', context)


@login_required
def reservation_list(request):
    """View user's reservations."""
    reservations = Reservation.objects.filter(user=request.user).order_by('date', 'time')
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        reservations = reservations.filter(status=status_filter)
    
    context = {
        'reservations': reservations,
        'status_filter': status_filter,
    }
    return render(request, 'restaurant/reservation_list.html', context)


@login_required
def reservation_detail(request, pk):
    """View reservation details."""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'restaurant/reservation_detail.html', context)


@login_required
def reservation_update(request, pk):
    """View for updating a reservation."""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    if reservation.status in ['cancelled', 'completed']:
        messages.error(request, 'Cannot update a cancelled or completed reservation.')
        return redirect('restaurant:reservation_detail', pk=reservation.pk)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reservation updated successfully!')
            return redirect('restaurant:reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm(instance=reservation)
    
    context = {
        'form': form,
        'reservation': reservation,
        'title': 'Update Reservation',
    }
    return render(request, 'restaurant/reservation_form.html', context)


@login_required
def reservation_delete(request, pk):
    """View for cancelling a reservation."""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, 'Reservation cancelled successfully!')
        return redirect('restaurant:reservation_list')
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'restaurant/reservation_confirm_delete.html', context)
