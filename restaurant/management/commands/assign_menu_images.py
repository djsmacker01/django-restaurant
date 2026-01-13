from django.core.management.base import BaseCommand
from restaurant.models import MenuItem
from django.core.files import File
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Assign images to existing menu items from media/menu_images/ folder'

    def handle(self, *args, **options):
        self.stdout.write('Assigning images to menu items...')
        
        # Mapping of menu item names to image filenames
        image_mapping = {
            'Caesar Salad': 'caesar-salad.jpg',
            'Bruschetta': 'Bruschetta.jpg',
            'Mozzarella Sticks': 'Mozzarella.jpg',
            'Soup of the Day': 'soap_of_d_day.jpg',
            'Chicken Wings': 'buffaloWings.jpg',
            'Grilled Salmon': 'skillet-seared-salmon-lemon-butter-sauce-4.jpg',
            'Beef Tenderloin': 'Beef_Tenderloin.jpeg',
            'Margherita Pizza': 'Margherita_Pizza.webp',
            'Chicken Parmesan': 'Chicken-Parmesan-Recipe-1.webp',
            'Fish and Chips': 'Fis_crispy_chips.jpg',
            'Vegetarian Risotto': 'Vegetarian_Risotto.jpg',
            'BBQ Ribs': 'BBQ_Ribs.jpg',
            'Chocolate Lava Cake': 'Chocolate_Cake.jpg',
            'Tiramisu': 'Tiramisu.webp',
            'New York Cheesecake': 'Perfect-New-York-Cheesecake-4.webp',
            'Apple Pie': 'Apple-Pie.jpg',
            'Ice Cream Sundae': 'Ice_Cream_Sundae.webp',
            'Red Wine': 'House_selection_of_premium_red_wine..jpeg',
            'White Wine': 'white_whine.jpg',
            'Fresh Orange Juice': 'Homemade-Orange-Juice.jpg',
            'Espresso': 'Espresso-coffee-Italian-breakfast-4.jpg',
            'Cappuccino': 'Cappuccino.jpg',
            'Coca Cola': 'Coca_Cola.jpg',
            'Craft Beer': 'Craft_Beer.jpg',
        }
        
        media_path = os.path.join(settings.BASE_DIR, 'media', 'menu_images')
        assigned_count = 0
        
        for item_name, image_filename in image_mapping.items():
            try:
                item = MenuItem.objects.get(name=item_name)
                
                # Skip if item already has an image
                if item.image:
                    self.stdout.write(
                        self.style.WARNING(f'  ⏭ {item.name} already has an image')
                    )
                    continue
                
                image_path = os.path.join(media_path, image_filename)
                
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        item.image.save(image_filename, File(f), save=True)
                    assigned_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Assigned image to: {item.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Image not found: {image_path}')
                    )
            except MenuItem.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠ Menu item not found: {item_name}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Error assigning image to {item_name}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Assigned {assigned_count} images to menu items')
        )
