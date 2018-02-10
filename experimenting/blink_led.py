# Blink an LED connected from GPIO 17 (pin 11) to ground (pin 6)

""" SETUP  """
import RPi.GPIO as GPIO
import time

def blink(pin):

    for i in range(0,4):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(0.25)
    for i in range(0,10):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(0.05)
    return
    

LED_pin = 11

# use RPi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set up GPIO output channel
GPIO.setup(LED_pin,GPIO.OUT)


""" START DOING THINGS """

# run the blink function
blink(LED_pin)
GPIO.cleanup()
