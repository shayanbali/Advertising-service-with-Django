# Advertising-service-with-Django
This project has been implemented for the cloud computing course of Amirkabir Computer Engineering Faculty. You can also see the project description and
my documentation about this project in this repo
\
\
In this project, i implemented an Advertising service with Django. My service Contains two subservices:
- Ad Registeration and Retrival
- Processing Ads


## Ad Registeration and Retrival
This subservice contains two API:
- Ad Registeration:
  1. This API receives the information of an ad including text, image and the sender's email.
  2. The information of this ad, including the text and email address of the sender, is stored in the database and a unique identifier is considered for it.
  3. It stores the image in an object storage. We choose the name of the image in this storage so that we can retrieve the image of an ad based on its identifiers.
  4. This API writes the ad ID for processing in the RabbitMQ queue.
  5. Send a response to user's request.
  
- Ad Retrival:
  1. This API receives the ID of an ad.
  2. If the ID related to an ad has not been checked, in response, a message like "Your ad is in the review queue" will be sent to the user.
  3. If the ID related to an ad is rejected, a message like "Your ad was not approved" will be given in response.
  4. If this ID corresponds to a verified ad, the information of this ad including text, image, category and status will be returned in the response.
  
## Processing Ads
The task of this service is to read advertisements from the RabbitMQ queue, process them and save the result on the database.
  1. This service connects to the RabbitMQ queue and listens for new messages. Each message corresponds to a registered notification.
  2. Each message read from the queue contains an advertisement ID. With this ID, the ad photo is received from the object storage.
  3. The ad photo is sent to photo tagging service 4 for processing. From the response of the tagging service, the first tag as Ad category is selected. Put this category in the category column of the database.
  4. By using the email sending service, an email is sent to the user to inform the user of the status (approval or rejection) of his ad.
  
  
## Implemented architecture
I used an architecture like following picture to implement this project:
\
\
![architecture](https://user-images.githubusercontent.com/58389567/220432149-bee98218-2165-4255-830a-f9993b86ddaf.jpg)


