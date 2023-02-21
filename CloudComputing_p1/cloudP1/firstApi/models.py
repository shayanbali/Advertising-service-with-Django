from django.db import models


class Ads(models.Model):
    description = models.CharField(max_length=400)
    email = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True, default='pending')
    category = models.CharField(max_length=100, blank=True, null=True)
    img = models.CharField(max_length=100, blank=True, null=True)





