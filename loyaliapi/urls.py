from django.conf.urls import url
from views import MobileUserAPI

urlpatterns = [

    url(r'^mobile/users/', MobileUserAPI.as_view(), name='mobile_user'),


]
