from django.db import models

class Service(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    price = models.FloatField(verbose_name="Price")

    def __str__(self):
        return f"{self.name} ({self.price} €)"


class Car(models.Model):
    make = models.CharField(verbose_name="Make", max_length=200)
    model = models.CharField(verbose_name="Model")
    license_plate = models.CharField(verbose_name="License plate")
    vin_code = models.CharField(verbose_name='VIN code')
    client_name = models.CharField(verbose_name="Client name")

    def __str__(self):
        return f"{self.make} {self.model}"


class Order(models.Model):
    date = models.DateField(verbose_name="Date")
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.date} – {self.car}"


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.service} x {self.quantity}"