from django.test import TestCase
from django.urls import reverse

from restaurant.models import Menu

# Create your tests here.


class MenuViewTest(TestCase):
    def setUp(self):
        # Set up some test instances of the Menu model
        Menu.objects.create(title="Pizza", price=10, inventory=5, menu_item_description="Good!")
        Menu.objects.create(title="Burger", price=8, inventory=7, menu_item_description="Nice!")
        Menu.objects.create(title="Salad", price=6, inventory=9, menu_item_description="Perfect!")
        

    def test_getall(self):
        response = self.client.get(reverse("api-menu"))
        self.assertEqual(response.status_code, 200)

        serialized_data = response.json()
        menu_objects = Menu.objects.all()
        
        expected_data = {
            "count": menu_objects.count(),
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": menu.id,
                    "title": menu.title,
                    "price": str(menu.price),
                    "inventory": menu.inventory,
                    "menu_item_description": menu.menu_item_description,
                } for menu in menu_objects
            ]
        }

        self.assertEqual(serialized_data, expected_data)


     