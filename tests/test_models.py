from django.test import TestCase

from restaurant.models import Menu
# Create your tests here.

class MenuTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="IceCream", price=80, inventory=100)
        itemstr = item.get_item()
        self.assertEqual(itemstr, "IceCream : 80")



# python manage.py test ile tests klasörü içindeki tüm testler çalıştırılır. Özellikle bir tanesini çalıştırmak istersen "python manage.py test tests.test_models"   diyebilirsin.
# Django'nun testleri çalıştırırken test dosyalarını nasıl bulduğunu belirleyen birkaç yapılandırma ayarı vardır. Bunlar arasında TEST_APPS, TEST_DIRS ve TEST_DISCOVER_PATTERN gibi ayarlar bulunur. Varsayılan olarak, Django test çerçevesi tests adlı bir klasörü otomatik olarak arar.
