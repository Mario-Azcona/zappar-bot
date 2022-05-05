from time import sleep
import os

import pycurl
import certifi
from io import BytesIO 
import json
import smtplib
from email.message import EmailMessage

import random

#thresholds = [1000,2000,2500,3500,4500,5500,6500,7500,8500,9500,10500]
thresholds = [150,160,170,180,190,200]
current_threshold = 0

def getTotalView():
    b_obj = BytesIO() 
    crl = pycurl.Curl() 

    crl.setopt(crl.URL, os.environ["url"])

    crl.setopt(pycurl.CAINFO, certifi.where())
    # Write bytes that are utf-8 encoded
    crl.setopt(crl.WRITEDATA, b_obj)
    # Perform a file transfer 
    crl.perform() 
    # End curl session
    crl.close()
    # Get the content stored in the BytesIO object (in byte characters) 
    get_body = b_obj.getvalue()

    body = get_body.decode('utf8')
    total_views = json.loads(body)["Total"]
    return total_views

def sendViewsWarning(number):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ["sender-email"]
    receiver_email = [os.environ["receiver_email-1"]]
    password = os.environ["password"]

    msg = EmailMessage()
    msg.set_content('Este mensaje ha sido programado para ser lanzado cuando se alcanza cierta cantidad de visualizaciones totales en la expo de realidad aumentada de Amanece en Animayo.\nEn los últimos minutos se ha superado el umbral de {} visualizaciones totales.'.format(number))
    msg['Subject'] = 'Realidad aumentada Animayo: Aviso de {} visualizaciones'.format(number)
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()

views = getTotalView()
while thresholds[current_threshold] <= views:
    current_threshold += 1

while 1:
    views = getTotalView()
    print("Current views: {}. Current threshold: {}".format(views,thresholds[current_threshold]))
    if  views >= thresholds[current_threshold]:
        print("WARNING:Sent email")
        sendViewsWarning(views)
        current_threshold += 1
    sleep(random.randint(1, 9) * 60)
