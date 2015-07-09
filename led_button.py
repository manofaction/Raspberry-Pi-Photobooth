# Listen for a press from momentary switch (GPIO-23 / pin 16 - GND), then:
# Blink an LED connected from GPIO 17 (pin 11) to ground (pin 6)

""" SETUP  """
import RPi.GPIO as GPIO
import time

LED_pin = 11
switch_pin = 16

# use RPi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set up GPIO output channel
GPIO.setup(LED_pin,GPIO.OUT)

# set up switch
GPIO.setup(switch_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

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

def take_picture():
    print('*Click*')
    
def my_callback(channel):
    blink(LED_pin)
    take_picture()

""" START DOING THINGS """

# run the blink function

GPIO.add_event_detect(switch_pin,
                      GPIO.RISING,
                      callback=my_callback,
                      bouncetime=999
                      )

try:
    time.sleep(100)
except KeyboardInterrupt:
    GPIO.cleanup()
    print('See ya!')

   
GPIO.cleanup()



















