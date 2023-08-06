from django.db import models

# Create your models here.
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    menu_item_description = models.TextField(max_length=1000, default='') 
    inventory = models.IntegerField()

    def __str__(self) -> str:
        return self.title

    def get_item(self):
        return f'{self.title} : {str(self.price)}'

"""
`__str__()` metodu, bir nesnenin metinsel temsilini döndüren özel bir metottur. Bu metodun `return f'{self.title}'` ifadesiyle belirtilen amacı, `MenuItem` modelinin her bir nesnesinin string temsilini, nesnenin `title` özelliğinin değeri olarak döndürmektir. Yani, `str()` fonksiyonu veya bir string ifadesi gerektiren herhangi bir yerde `MenuItem` nesnesi çağrıldığında, bu metot otomatik olarak çağrılır ve nesnenin `title` özelliğinin değeri döndürülür. Genel olarak __str__ metodu, daha genel bir nesne temsilini sağlamak için kullanıldığından, özel bir temsil gerektiğinde get_item metodu tercih edilebilir.
"""

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=255)
    no_of_guests = models.IntegerField()
    booking_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)
    
    def __str__(self) -> str:
        return f"{self.name} - {self.no_of_guests} guests"