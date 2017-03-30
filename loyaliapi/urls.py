from django.conf.urls import url
from views import MobileUserAPI, CheckUserCredentials, \
    AddSubscription, CustomerSubscriptionAPI, VendorByIDAPI

urlpatterns = [

    url(r'^login/', CheckUserCredentials.as_view(), name='mobile_login'),

    url(r'^mobile/users/', MobileUserAPI.as_view(), name='mobile_user'),

    url(r'^mobile/subscriptions/', CustomerSubscriptionAPI.as_view(), name='customer_subscriptions'),

    url(r'^mobile/vendorByID/', VendorByIDAPI.as_view(), name='vendor_by_id'),

    url(r'^createSubscription/', AddSubscription.as_view(), name='create_subscription'),



]
