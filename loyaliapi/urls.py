from django.conf.urls import url
from loyaliapi.views import MobileUserAPI, CheckUserCredentialsAPI, AddSubscriptionAPI, \
    VendorByIdAPI, VendorsWithCardsAPI, CustomersCardsAPI, AllCustomersSubscriptionsAPI, \
    SingleSubscriptionAPI, TestingAPI, DeleteSubscriptionAPI, PunchCardAPI, \
    CustomerRewardsAPI, RedeemReward, AllPurchases


urlpatterns = [

    url(r'^login/', CheckUserCredentialsAPI.as_view(), name='mobile_login'),

    url(r'^mobile/subscriptions/byCardID/', SingleSubscriptionAPI.as_view(), name='customer_subscriptions_by_card'),

    url(r'^mobile/subscriptions/', AllCustomersSubscriptionsAPI.as_view(), name='customer_subscriptions'),

    url(r'^mobile/users/', MobileUserAPI.as_view(), name='mobile_user'),

    url(r'^mobile/vendorByID/', VendorByIdAPI.as_view(), name='vendor_by_id'),

    url(r'^createSubscription/', AddSubscriptionAPI.as_view(), name='create_subscription'),

    url(r'^deleteSubscription/', DeleteSubscriptionAPI.as_view(), name='delete_subscriptions'),

    url(r'^mobile/vendorsAndCards/', VendorsWithCardsAPI.as_view(), name='customers_vendors_and_cards'),

    url(r'^customer/allPurchases/', AllPurchases.as_view(), name='all_purchases'),

    url(r'^mobile/rewards/', CustomerRewardsAPI.as_view(), name='customer_rewards'),

    url(r'^mobile/customerCards/', CustomersCardsAPI.as_view(), name='customers_cards'),

    url(r'^mobile/punchCard/', PunchCardAPI.as_view(), name='punch_card'),

    url(r'^mobile/redeemReward/', RedeemReward.as_view(), name='redeem_reward'),

    url(r'^testingAPI/', TestingAPI.as_view(), name='testing_api'),

]
