from django.contrib import admin

# Register your models here.
from loyali.models import Subscription, Card, CardsInUse, Rewards, Vendor, VendorUser
from loyaliapi.models import MobileUser

admin.site.register(Subscription)

admin.site.register(Rewards)
admin.site.register(VendorUser)
admin.site.register(MobileUser)


class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'store_name')


class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'max', 'description')


class CardsInUseAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'current')


admin.site.register(Card, CardAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CardsInUse, CardsInUseAdmin)

