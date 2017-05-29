from django.contrib import admin

# Register your models here.
from loyali.models import Subscription, Card, CardsInUse, Rewards, Vendor, VendorUser, \
    Purchase
from loyaliapi.models import MobileUser

admin.site.register(Subscription)
admin.site.register(VendorUser)
admin.site.register(MobileUser)


class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'store_name')


class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'max', 'description', 'type')


class CardsInUseAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'current')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'customer', 'type', 'date')


class RewardsAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vendor', 'type', 'amount')


admin.site.register(Card, CardAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CardsInUse, CardsInUseAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Rewards, RewardsAdmin)

