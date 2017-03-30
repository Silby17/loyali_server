from django.contrib import admin

# Register your models here.
from loyali.models import Subscription, Card, CardsInUse, Rewards, Vendor, VendorUser
from loyaliapi.models import MobileUser

admin.site.register(Subscription)
admin.site.register(Card)
admin.site.register(CardsInUse)
admin.site.register(Rewards)
admin.site.register(Vendor)
admin.site.register(VendorUser)
admin.site.register(MobileUser)
