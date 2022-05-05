from time import sleep
import os

import pycurl
import certifi
from io import BytesIO 
import json
import smtplib
from email.message import EmailMessage

import random

thresholds = [500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000,10500]
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
    receiver_email = [os.environ["receiver_email-1"],os.environ["receiver_email-2"],os.environ["receiver_email-3"],os.environ["receiver_email-4"]]
    password = os.environ["password"]

    msg = EmailMessage()
    msg.set_content('Este mensaje ha sido programado para ser lanzado cuando se supera cierto cantidad de visualizaciones totales en la expo de realidad aumentada de Amanece en Animayo.\nEn los últimos minutos se ha superado el umbral de {} visualizaciones totales.'.format(number))
    msg['Subject'] = 'Realidad aumentada Animayo: Aviso de {} visualizaciones'.format(number)
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()

def sendTestMail():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ["sender-email"]
    receiver_email = [os.environ["receiver_email-1"]]
    password = os.environ["password"]

    msg = EmailMessage()
    msg.set_content('Este mensaje ha sido programado para ser lanzado cuando se inicia el bot de la expo de realidad aumentada de Amanece en Animayo.')
    msg['Subject'] = 'Realidad aumentada Animayo: Mail de prueba'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()

views = getTotalView()
while thresholds[current_threshold] <= views:
    current_threshold += 1

sendTestMail()

while 1:
    views = getTotalView()
    print("Current views: {}. Current threshold: {}".format(views,thresholds[current_threshold]))
    if  views >= thresholds[current_threshold]:
        print("WARNING:Sent email")
        sendViewsWarning(views)
        current_threshold += 1
    sleep(random.randint(1, 9) * 60)
