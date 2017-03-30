from django.conf.urls import url
from views import index, login, admin_main, vendor_main, contact_us, logout, \
    vendor_add, VendorAPI, admin_user_page, view_vendors, AdminUserAPI, saved_page, \
    redirect_to_main, view_users_page, full_vendors_page, delete_vendors, \
    vendor_customers, AddCardAPI, GetVendorsCardsAPI

urlpatterns = [

    url(r'^$', index, name='index'),

    url(r'^login/', login, name='login'),

    url(r'^admin/mainmenu', admin_main, name='admin_main'),

    url(r'^redirect/mainmenu/', redirect_to_main, name='redirect_main'),

    url(r'^admin/users/', AdminUserAPI.as_view(), name='admin_users'),

    url(r'^admin/viewusers/', view_users_page, name='view_users'),

    url(r'^admin/add_user/', admin_user_page, name='add_admin-user'),

    url(r'^admin/vendors', view_vendors, name='view_vendors'),

    url(r'^admin/deleteVendors', delete_vendors, name='delete_vendors'),

    url(r'^vendor/mainmenu', vendor_main, name='vendor_main'),

    url(r'^vendor/customers', vendor_customers, name='vendor_customers'),

    url(r'^vendor/addCard/', AddCardAPI.as_view(), name='vendor_add_card'),

    url(r'^vendor/viewCards/', GetVendorsCardsAPI.as_view(), name='view_cards'),

    url(r'^vendor/', VendorAPI.as_view(), name='vendors'),

    url(r'^add/vendor', vendor_add, name='vendor_add'),

    url(r'^contact', contact_us, name='contact'),

    url(r'^logout/', logout, name='logout'),

    url(r'^saved/', saved_page, name='saved'),

    url(r'^fullvendors/', full_vendors_page, name='full_vendors'),
]
