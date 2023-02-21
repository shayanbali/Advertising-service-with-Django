from django.core.files.storage import default_storage
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import AdsSerializer
from .models import Ads
from .rabbitMQ import sendID_rabbit, editUrl
import basehash

bucket_url = 'https://shayan-bucket.s3.amazonaws.com/'


class AdsViewSet(APIView):
    def get(self, req, *args, **kwargs):
        serializer = AdsSerializer(Ads.objects.get(id=req.data.get('id')))
        data = "Nothing"
        state = serializer.data.get('state')
        if state == 'confirmed':
            data = serializer.data
        res = {"AD_status": state, "AD_data": data}
        return Response(res, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = AdsSerializer(data=req.data)
        if not serializer.is_valid():
            return Response({"status": "BAD REQUEST", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            try:
                img = req.FILES.get('image', '')
                hash_fn = basehash.base36()
                hashed_id = hash_fn.hash(serializer.data['id'])
                img_id = str(hashed_id) + '.png'
                default_storage.save(img_id, img)
                img_url = bucket_url + img_id
                editUrl(img_url, serializer.data['id'])


            except:
                img = None

            sendID_rabbit(serializer.data['id'])
            return Response({"status": "successful", "data": serializer.data}, status=status.HTTP_200_OK)
