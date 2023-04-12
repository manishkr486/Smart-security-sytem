import RPi.GPIO as GPIO
import time as t
from mfrc522 import SimpleMFRC522
import smtplib
import picamera
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def validation():
    valid = [1081313927759, 764207711048] #rfid number yours will be different
    GPIO.setup(20,GPIO.OUT)
    if id in valid:
        print("Entry Accepted")
        GPIO.output(20,True)
        t.sleep(5)
        GPIO.output(20,False)
        return "Person Entry Accepted"
    else:
        print("Entry Denied")
        return "Person Entry Denied"

def email(message):
    # Define email credentials and recipient
    to_email = 'your email ID'
    password = 'email password'
    from_email = "sender's email"
    # Take a picture with the Raspberry Pi camera module
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.capture('/home/pi/image.jpg')
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = message
    with open('/home/pi/image.jpg', 'rb') as f:
        img = MIMEImage(f.read())
        msg.attach(img)
    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print('Something went wrong:', e)

# reading Tag
reader = SimpleMFRC522()

try:
    print('Place Your Tag')
    id,text= reader.read()
    m=validation()
    email(m)
    print("ID : ",id)
    print("Name : ",text) 
finally: 
    GPIO.cleanup()







