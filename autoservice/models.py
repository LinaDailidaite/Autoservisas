from django.db import models

class Service(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    price = models.FloatField(verbose_name="Price")

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

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
    date = models.DateField(verbose_name="Date", auto_now_add=True)
    car = models.ForeignKey(to="Car", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.car} ({self.date})"

    def total(self):
        return sum(line.line_sum() for line in self.lines.all())

    total.short_description = "Total (€)"


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(to="Service", on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.service} x {self.quantity}"

    def line_sum(self):
        return float(self.quantity * self.service.price)
    line_sum.short_description = "Line sum (€)"
