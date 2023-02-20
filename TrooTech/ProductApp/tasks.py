import asyncio
from celery import shared_task
from time import time, sleep
from django.core.mail import send_mail,EmailMessage
from  django.conf import settings


@shared_task(bind=True)
def sendMailTask(self,fileName,duration=0):
   subject= 'Product data using Celery - TrootechProject'
   message= 'Please find attached sheet of Product data'
   receiver= ['shet8961@gmail.com','shahsilvi06@gmail.com']
   #change here
   asyncio.run(mainCoroutine(duration, subject,message,receiver,fileName))


async def subCoroutine(duration,subject,message,receivers,fileName):
   sleep(duration)
   sendMailWithAttatchment(subject,message,receivers,fileName)


async def mainCoroutine(duration, subject,message,receiver,fileName):
   coroutine_object = subCoroutine(duration, subject,message,receiver,fileName)
   await coroutine_object


def sendMailWithAttatchment(subject,message,receivers,fileName):
   mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, receivers)
   with open(fileName) as f:
      mail.attach(f.name,f.read())
      mail.send()
      print("Sent mail")