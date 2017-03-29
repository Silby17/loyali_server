from django.conf.urls import url
from views import MobileUserAPI, CheckUserCredentials

urlpatterns = [

    url(r'^mobile/users/', MobileUserAPI.as_view(), name='mobile_user'),

    url(r'^login/', CheckUserCredentials.as_view(), name='mobile_login'),

]
