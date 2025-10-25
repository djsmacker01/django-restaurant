from django.shortcuts import render
from .models import MenuItem


# Create your views here.
def menu_list(request):
    """
    View function for displaying the menu list.
    """
     # Get all menu items from database
    menu_items = MenuItem.objects.all()

    # Prepare data to send to template
    context = {
        'menu_items': menu_items
    }
   
   #render the template with the data
    return render(request, 'restaurant/menu_list.html', context)