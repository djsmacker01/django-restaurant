from django.shortcuts import render
from .models import MenuItem



def menu_list(request):
    """
    View function for displaying the menu list.
    """
     # Get all menu items from database
    menu_items = MenuItem.objects.all()
e
    context = {
        'menu_items': menu_items
    }
   
 
    return render(request, 'restaurant/menu_list.html', context)
