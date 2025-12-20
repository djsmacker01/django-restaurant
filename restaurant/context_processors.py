def cart_count(request):
    """Context processor to add cart item count to all templates."""
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = request.user.orders.get(status='pending', payment_status='pending')
            cart_count = cart.order_items.count()
        except:
            pass
    return {'cart_count': cart_count}










