from django.conf.urls import url
from views import index, login, admin_main, vendor_main, contact_us, logout,\
    vendor_add, VendorAPI, add_admin_user, view_vendors

urlpatterns = [

    url(r'^$', index, name='index'),

    url(r'^login/', login, name='login'),

    url(r'^admin/mainmenu', admin_main, name='admin_main'),

    url(r'^admin/vendors', view_vendors, name='view_vendors'),

    # POST will create a new Vendor user
    # GET will return a list of all vendors
    url(r'^vendor/', VendorAPI.as_view()),

    url(r'^add/vendor', vendor_add, name='vendor_add'),

    url(r'^vendor/mainmenu', vendor_main, name='vendor_main'),

    url(r'^contact', contact_us, name='contact'),

    url(r'^logout/', logout, name='logout'),

    url(r'^addUser/', add_admin_user, name='add_admin_user'),

]
