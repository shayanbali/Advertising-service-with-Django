import mysql.connector
import requests

HOST = "mysql-cc-hw1-shayanbali-shayanbali3-bfff.aivencloud.com"
PORT = 27978
USER = "avnadmin"
PASSWORD = "AVNS_9XBFtm4jwXZQkSpUlig"
DATABASE = "defaultdb"

mydb = mysql.connector.connect(
    host=HOST,
    port=PORT,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

mycursor = mydb.cursor(buffered=True)

# mycursor.execute(
#     "CREATE TABLE ads (id MEDIUMINT NOT NULL AUTO_INCREMENT primary key, description VARCHAR(255), email VARCHAR(255) NOT NULL, state VARCHAR(255) default 'pending', category VARCHAR(255))"
# )


# mycursor.execute("DELETE FROM firstApi_ads where id > 0")
mydb.commit()
mycursor.execute("SELECT * FROM firstApi_ads")
myresult = mycursor.fetchall()

for x in myresult:
    print(x)


def new_ad(des, myEmail):
    mycursor = mydb.cursor()

    sql = "INSERT INTO ads (description, email) VALUES (%s, %s)"
    val = (des, myEmail)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT id FROM ads ORDER BY id DESC LIMIT 1")
    id_new_ad = mycursor.fetchall()
    return id_new_ad


def editState(state, category, imageId):
    mydb = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    mycursor = mydb.cursor(buffered=True)
    sql = 'UPDATE firstApi_ads SET state = (%s), category = (%s) WHERE id = (%s)'
    val = (state, category, imageId)
    mycursor.execute(sql, val)

    mydb.commit()


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


def getURL_fromID(image_ID):
    mydb = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    mycursor = mydb.cursor(buffered=True)





    print(int(image_ID), "image id")
    sql = 'SELECT img from firstApi_ads where id = (%s)'
    val = (int(image_ID),)
    mycursor.execute(sql, val)
    image_url = mycursor.fetchall()
    print(image_url)
    final_URL = ""
    if len(image_url) > 0:
        final_URL = image_url[0][0]
    print(final_URL, "final url")
    return final_URL


def sendMail(id, state):
    mydb = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    mycursor = mydb.cursor(buffered=True)
    sql = 'SELECT email from firstApi_ads where id = (%s)'
    val = (id,)
    mycursor.execute(sql, val)
    email = mycursor.fetchall()
    email = email[0][0]
    extra_info = "\n"
    if state == 'confirmed':
        sql = 'SELECT category from firstApi_ads where id = (%s)'
        val = (id,)
        mycursor.execute(sql, val)
        category = mycursor.fetchall()
        category = category[0][0]
        extra_info += ("category: " + category + "\n")

        sql = 'SELECT description from firstApi_ads where id = (%s)'
        val = (id,)
        mycursor.execute(sql, val)
        description = mycursor.fetchall()
        description = description[0][0]
        extra_info += ("description: " + description + "\n")

        sql = 'SELECT img from firstApi_ads where id = (%s)'
        val = (id,)
        mycursor.execute(sql, val)
        img = mycursor.fetchall()
        img = img[0][0]
        extra_info += ("imageURL: " + img + "\n")

    return requests.post(
        "https://api.mailgun.net/v3/sandbox34c6beeb94f7428e82cfb280da19e798.mailgun.org/messages",
        auth=("api", "d65313ed96d0e7bbee06a148ccf30bc5-2de3d545-f0188fe7"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox34c6beeb94f7428e82cfb280da19e798.mailgun.org>",
              "to": [email],
              "subject": 'Advertisement state',
              "text": 'advertisement id : ' + id + '\n the AD has been ' + state+extra_info})
