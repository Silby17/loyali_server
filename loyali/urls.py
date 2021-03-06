from django.conf.urls import url, include
from loyali.views import index, login, admin_main, vendor_main, contact_us, logout, \
    vendor_add, VendorAPI, admin_user_page, view_vendors, AdminUserAPI, saved_page, \
    redirect_to_main, view_users_page, full_vendors_page, delete_vendors, \
    vendor_customers, AddCardAPI, VendorsCardsAPI, vendors_customer_rewards, \
    customer_rewards_by_id, all_purchases, customer_purchase_by_id, change_password, \
    message_menu, pubnub_vendor_send_batch_message, pubnub_send_single_message, \
    VendorCustomersAPI, message_sent, pubnub_admin_send_batch_message

urlpatterns = [

    url(r'^$', index, name='index'),

    url(r'^login/', login, name='login'),

    url(r'^sent/', message_sent, name='sent'),

    url(r'^admin/mainmenu', admin_main, name='admin_main'),

    url(r'^redirect/mainmenu/', redirect_to_main, name='redirect_main'),

    url(r'^admin/users/', AdminUserAPI.as_view(), name='admin_users'),

    url(r'^admin/viewusers/', view_users_page, name='view_users'),

    url(r'^vendor/customersAPI/', VendorCustomersAPI.as_view(), name='vendors_customers_API'),

    url(r'^admin/add_user/', admin_user_page, name='add_admin-user'),

    url(r'^admin/vendors', view_vendors, name='view_vendors'),

    url(r'^admin/deleteVendors', delete_vendors, name='delete_vendors'),

    url(r'^vendor/mainmenu', vendor_main, name='vendor_main'),

    url(r'^message/menu', message_menu, name='message_menu'),

    url(r'^message/batch', pubnub_vendor_send_batch_message, name='vendor_batch_message'),

    url(r'^admin/batch', pubnub_admin_send_batch_message, name='admin_batch_message'),

    url(r'^message/singleMessage', pubnub_send_single_message, name='simple_single_message'),

    url(r'^vendor/settings/changePassword', change_password, name='change_password'),

    url(r'^vendor/rewards/byID/(?P<customer_id>[0-9]+)/$', customer_rewards_by_id,
        name='customer_rewards_per_id'),

    url(r'^vendor/purchases/byID/(?P<customer_id>[0-9]+)/$', customer_purchase_by_id,
        name='customer_purchase'),

    url(r'^vendor/customers', vendor_customers, name='vendor_customers'),

    url(r'^vendor/allPurchases', all_purchases, name='vendor_purchases'),

    url(r'^vendor/addCard/', AddCardAPI.as_view(), name='vendor_add_card'),

    url(r'^vendor/viewCards/', VendorsCardsAPI.as_view(), name='view_cards'),

    url(r'^vendor/rewards/', vendors_customer_rewards, name='vendor_rewards'),

    url(r'^vendor/', VendorAPI.as_view(), name='vendors'),

    url(r'^add/vendor', vendor_add, name='vendor_add'),

    url(r'^contact', contact_us, name='contact'),

    url(r'^logout/', logout, name='logout'),

    url(r'^saved/', saved_page, name='saved'),

    url(r'^fullvendors/', full_vendors_page, name='full_vendors'),

]
