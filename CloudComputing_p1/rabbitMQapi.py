import json

import os


import pika, sys, os


from tagging import tagImage
from database import sendMail, editState, getURL_fromID
import basehash


import os


AMQP_URL = "amqps://yivdzdak:m8d9DdDZB9S5E_sNXeCMRVqMvgUg3vSI@toad.rmq.cloudamqp.com/yivdzdak"
bucket_url = 'https://shayan-bucket.s3.amazonaws.com/'


# t = Ads.objects.get(id=1)
# t.value = 999  # change field
# t.save()  # this will update only


# def editState(state, category, imageID):
#     myAd = Ads.objects.get(id=int(imageID))
#     myAd.category = category
#     myAd.state = state
#     myAd.save()  # this will update


# def sendID_rabbit(adID):
#     connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
#     channel = connection.channel()
#     channel.queue_declare(queue='ad_ids')
#
#     hash_fn = basehash.base36()
#     hash_id = hash_fn.hash(adID)
#
#     channel.basic_publish(exchange='', routing_key='ad_ids', body=hash_id)
#     connection.close()


def receiveID_rabbit():
    connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = connection.channel()

    channel.queue_declare(queue='ad_ids')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        print(body, "    body")
        # image url from s3
        imageID = str(body).replace('b', '').replace('\'', '')
        # hash_fn = basehash.base36()
        # hash_value = hash_fn.hash(13)
        # imageID_hashed = hash_fn.hash(imageID)
        # image_url = bucket_url + imageID_hashed + '.png'

        image_url = getURL_fromID(imageID)
        # send it to tagging system
        state, category = tagImage(image_url)
        editState(state, category, imageID)
        # send email
        req = sendMail(imageID, state)

    channel.basic_consume(queue='ad_ids', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


try:
    receiveID_rabbit()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

