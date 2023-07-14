from django.db import models

# Create your models here.
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()

    def __str__(self) -> str:
        return self.title


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=255)
    no_of_guests = models.IntegerField()
    booking_date = models.DateTimeField()
    
    def __str__(self) -> str:
        return f"{self.name} - {self.no_of_guests} guests"