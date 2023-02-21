from rest_framework import serializers

from .models import Ads


class AdsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ads
        fields = ('id', 'description', 'email', 'state', 'category', 'img')
