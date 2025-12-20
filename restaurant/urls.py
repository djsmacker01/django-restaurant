from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    # Home
    path('', views.menu_list, name='menu_list'),
    
    # Menu items
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/<int:pk>/', views.menu_detail, name='menu_detail'),
    path('menu/create/', views.menu_item_create, name='menu_item_create'),
    path('menu/<int:pk>/update/', views.menu_item_update, name='menu_item_update'),
    path('menu/<int:pk>/delete/', views.menu_item_delete, name='menu_item_delete'),
    
    # Cart and checkout
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/item/<int:item_id>/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/item/<int:item_id>/remove/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/invoice/', views.order_invoice, name='order_invoice'),
    
    # Reservations
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/create/', views.reservation_create, name='reservation_create'),
    path('reservations/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('reservations/<int:pk>/update/', views.reservation_update, name='reservation_update'),
    path('reservations/<int:pk>/delete/', views.reservation_delete, name='reservation_delete'),
]
