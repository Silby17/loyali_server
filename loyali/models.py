from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# This is the vendor Model
from loyaliapi.models import MobileUser


class Vendor(models.Model):
    store_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    store_type = models.CharField(max_length=100, null=True, blank=True)
    logo_title = models.FileField(null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:"
                                         "'+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=100, null=True, validators=[phone_regex],
                             blank=True)


# This is the Vendor user Model
class VendorUser(User):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='users')


class Subscription(models.Model):
    customer = models.ForeignKey(MobileUser, on_delete=models.CASCADE,
                                 related_name='subscriptions')
    vendor = models.ForeignKey(VendorUser, on_delete=models.CASCADE,
                               related_name='subscriptions')


class Card(models.Model):
    description = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='cards')
    max = models.IntegerField()


class CardsInUse(models.Model):
    customer = models.ForeignKey(MobileUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    current = models.IntegerField()


class Rewards(models.Model):
    customer = models.ForeignKey(MobileUser, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, blank=True)
    amount = models.IntegerField()
