from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.contrib import admin
from tinymce.models import HTMLField
from PIL import Image
import os
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    photo = models.ImageField(_("Photo"), upload_to="profile_pics", null=True, blank=True)

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

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Service(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    price = models.FloatField(verbose_name=_("Price"))

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return f"{self.name} ({self.price} €)"


class Car(models.Model):
    make = models.CharField(verbose_name=_("Make"), max_length=200)
    model = models.CharField(verbose_name=_("Model"), max_length=200)
    license_plate = models.CharField(verbose_name=_("License plate"), max_length=20)
    vin_code = models.CharField(verbose_name=_('VIN code'), max_length=50)
    client_name = models.CharField(verbose_name=_("Client name"), max_length=200)
    cover = models.ImageField(_('Cover'), upload_to='covers', null=True, blank=True)
    description = HTMLField(verbose_name=_("Description"), max_length=3000, default="")

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class Order(models.Model):
    date = models.DateField(verbose_name=_("Date"), auto_now_add=True)
    car = models.ForeignKey(to="Car", verbose_name=_("Car"), on_delete=models.SET_NULL, null=True, blank=True)
    reader = models.ForeignKey(to="CustomUser", verbose_name=_("Client"), on_delete=models.SET_NULL, null=True,
                               blank=True)
    due_back = models.DateField(verbose_name=_("Due back"), null=True, blank=True)

    @admin.display(boolean=True, description=_('Is on time / Delayed'))
    def is_on_time(self):
        if not self.due_back:
            return True
        return timezone.now().date() <= self.due_back

    LOAN_STATUS = (
        ('p', _('Confirmed')),
        ('v', _('In Progress')),
        ('i', _('Done')),
        ('at', _('Canceled')),
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=2,
        choices=LOAN_STATUS,
        blank=True,
        default='p',
        help_text=_('Order status'),
    )

    def __str__(self):
        return f"{self.car} ({self.date})"

    def total(self):
        return sum(line.line_sum() for line in self.lines.all())

    total.short_description = _("Total (€)")

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", verbose_name=_("Order"), on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(to="Service", verbose_name=_("Service"), on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name=_("Quantity"))

    def __str__(self):
        return f"{self.service} x {self.quantity}"

    def line_sum(self):
        return float(self.quantity * self.service.price)

    line_sum.short_description = _("Line sum (€)")

    class Meta:
        verbose_name = _('Order Line')
        verbose_name_plural = _('Order Lines')


class OrderReview(models.Model):
    order = models.ForeignKey(to="Order", verbose_name=_("Order"), on_delete=models.SET_NULL, null=True, blank=True,
                              related_name="reviews")
    reviewer = models.ForeignKey(to="CustomUser", verbose_name=_("Reviewer"), on_delete=models.SET_NULL, null=True,
                                 blank=True)
    date_created = models.DateTimeField(verbose_name=_("Date Created"), auto_now_add=True)
    content = models.TextField(verbose_name=_("Content"), max_length=2000)

    class Meta:
        verbose_name = _("Order Review")
        verbose_name_plural = _('Order Reviews')
        ordering = ['-date_created']