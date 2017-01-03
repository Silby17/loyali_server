from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class MobileUser(User):
    facebook_id = models.CharField(max_length=255, null=True, blank=True)
    push_api_key = models.CharField(max_length=255, null=True, blank=True)