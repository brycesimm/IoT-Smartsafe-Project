import RPi.GPIO as GPIO
import time
import I2C_LCD_driver
from time import *
import threading
import RepeatedTimer
from twilio.rest import Client

TWILIO_ACCOUNT_SID = "" # replace with your Account SID
TWILIO_AUTH_TOKEN = "" # replace with your Auth Token
TWILIO_PHONE_SENDER = "" # replace with the phone number you registered in twilio
TWILIO_PHONE_RECIPIENT = "" # replace with your phone number

# these GPIO pins are connected to the keypad
# change these according to your connections!
#L1-L4 are output, C1-C4 are input

L1 = 11
L2 = 13
L3 = 15
L4 = 19

C1 = 21
C2 = 23
C3 = 29
C4 = 31

servo = 38 #(PCM Pin) and 5V
pir = 8
lights = 7

# Initialize the GPIO pins

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
GPIO.setup(servo,GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pir, GPIO.IN)
GPIO.setup(lights,GPIO.IN)

p=GPIO.PWM(servo,50)# 50hz frequency

p.start(8)# starting duty cycle ( it set the servo to 0 degree )

#Variables

code = ""
setCode = "1234"
state = False
motion = False
light = False
mylcd = I2C_LCD_driver.lcd()

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    global code
    if(GPIO.input(C1) == 1):
        code = code + characters[0]
        #print(characters[0])
    if(GPIO.input(C2) == 1):
        code = code + characters[1]
        #print(characters[1])
    if(GPIO.input(C3) == 1):
        code = code + characters[2]
        #print(characters[2])
    if(GPIO.input(C4) == 1):
        code = code + characters[3]
        #print(characters[3])
    GPIO.output(line, GPIO.LOW)
def motionSense():
    global motion
    if motion == True:
        #print("\nMotion Detected!")
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
        to=TWILIO_PHONE_RECIPIENT,
        from_=TWILIO_PHONE_SENDER,
        body="Motion has been detected!")
        motion = False
def lightSense():
    global light
    if light == True:
        #print("\nLight Detected!")
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
        to=TWILIO_PHONE_RECIPIENT,
        from_=TWILIO_PHONE_SENDER,
        body="Light has been detected!")
        light = False

#Threads
        
m = RepeatedTimer.RepeatedTimer(20,motionSense)
l = RepeatedTimer.RepeatedTimer(20,lightSense)


sleep(2) #give motion sensor time to start
try:
    while True:
        if GPIO.input(pir) == True:      #If PIR pin goes high, motion is detected
            motion = True
        if GPIO.input(lights) == False:
            light = True
        # call the readLine function for each row of the keypad
        readLine(L1, ["1","2","3","A"])
        readLine(L2, ["4","5","6","B"])
        readLine(L3, ["7","8","9","C"])
        readLine(L4, ["*","0","#","D"])
        sleep(0.25)
        mylcd.lcd_display_string("Code: "+code)
        if(len(code) >= 4) :
            mylcd.lcd_clear()
            sleep(1)
            if(code == setCode) :
                if(not state): #if state is false (closed), then !state is true
                    mylcd.lcd_display_string("Unlocking")
                    sleep(0.75)
                    p.ChangeDutyCycle(2.5)
                    sleep(0.75)
                    state = not state
                else: #if state is true (open) then !state is false
                    mylcd.lcd_display_string("Closing")
                    sleep(0.75)
                    p.ChangeDutyCycle(8)
                    sleep(0.75)
                    state = not state
            else :
                mylcd.lcd_display_string("Wrong code")
                mylcd.lcd_display_string("Code reset",2,0)
                sleep(1)
            code = ""
            mylcd.lcd_clear()
            
except KeyboardInterrupt:
    print("\nApplication stopped!")
    mylcd.lcd_clear()
    p.ChangeDutyCycle(8)
    sleep(0.05)
    p.stop()
    m.stop()
    l.stop()
    GPIO.cleanup()
    exit()