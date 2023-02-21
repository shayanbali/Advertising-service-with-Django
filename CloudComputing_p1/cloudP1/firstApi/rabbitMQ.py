import json
import mysql.connector
import pika, sys, os

# from tagging import tagImage
# from database import editState, sendMail

AMQP_URL = "amqps://yivdzdak:m8d9DdDZB9S5E_sNXeCMRVqMvgUg3vSI@toad.rmq.cloudamqp.com/yivdzdak"
bucket_url = 'https://shayan-bucket.s3.amazonaws.com/'

HOST = "mysql-cc-hw1-shayanbali-shayanbali3-bfff.aivencloud.com"
PORT = 27978
USER = "avnadmin"
PASSWORD = "AVNS_9XBFtm4jwXZQkSpUlig"
DATABASE = "defaultdb"


def sendID_rabbit(adID):
    connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = connection.channel()
    channel.queue_declare(queue='ad_ids')
    channel.basic_publish(exchange='', routing_key='ad_ids', body=str(adID))
    connection.close()


def editUrl(img_url, imageId):

    mydb = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    mycursor = mydb.cursor(buffered=True)
    sql = 'UPDATE firstApi_ads SET img = (%s) WHERE id = (%s)'
    val = (img_url, imageId)
    mycursor.execute(sql, val)
    mydb.commit()


