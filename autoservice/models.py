from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.contrib import admin
from tinymce.models import HTMLField
from PIL import Image
import os

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="profile_pics", null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo and os.path.exists(self.photo.path):
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)

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
    cover = models.ImageField('Viršelis', upload_to='covers', null=True, blank=True)
    description = HTMLField(verbose_name="Description", max_length=3000, default="")

    def __str__(self):
        return f"{self.make} {self.model}"


class Order(models.Model):
    date = models.DateField(verbose_name="Date", auto_now_add=True)
    car = models.ForeignKey(to="Car", on_delete=models.SET_NULL, null=True, blank=True)
    reader = models.ForeignKey(to="autoservice.CustomUser", verbose_name="Reader", on_delete=models.SET_NULL, null=True, blank=True)
    due_back = models.DateField(verbose_name="Bus grąžinta", null=True, blank=True)
    @admin.display(boolean=True, description='Bus grąžinta laiku / Vėluoja')
    def is_on_time(self):
        if not self.due_back:
            return True
        return timezone.now().date() <= self.due_back
    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('i', 'Įvykdyta'),
        ('at', 'Atšaukta'),
    )

    status = models.CharField(
        max_length=2,
        choices=LOAN_STATUS,
        blank=True,
        default='p',
        help_text='Užsakymo statusas',
    )
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

class OrderReview(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Order", on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    reviewer = models.ForeignKey(to="autoservice.CustomUser", verbose_name="Reviewer", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    content = models.TextField(verbose_name="Content", max_length=2000)

    class Meta:
        verbose_name = "Order Review"
        verbose_name_plural = 'Order Reviews'
        ordering = ['-date_created']
