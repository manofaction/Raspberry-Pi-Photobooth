# Blink an LED connected from GPIO 17 (pin 11) to ground (pin 6)
# Also: Take picture using GPIO pins to 2.5mm remote jack

""" SETUP  """
import RPi.GPIO as GPIO
import time

global button_pressed
button_pressed = 0

# Set up which which pins are connected to things
LED_pin = 11
focus_pin = 22
shutter_pin = 12
switch_pin = 16

# Use RPi board pin numbers
GPIO.setmode(GPIO.BOARD)

# Set up GPIO input/output channels
GPIO.setup(LED_pin,GPIO.OUT)
GPIO.setup(focus_pin,GPIO.OUT)
GPIO.setup(shutter_pin,GPIO.OUT)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

"""
Ground: Base of plug (yellow)
Focus:  Middle (white)
Shutter: Tip of plug (red)

NOTE:  Make sure camera is in "single shot" mode, otherwise it will
       take multiple pics as long as "shutter" is connected to ground
"""

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

def focus_camera(pin):
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin,GPIO.LOW)
    return

def take_picture(pin):
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin,GPIO.LOW)
    return

def focus_and_blink(f_pin,l_pin):
    GPIO.output(f_pin,GPIO.HIGH)
    for i in range(0,4):
        GPIO.output(l_pin,GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(l_pin,GPIO.LOW)
        time.sleep(0.25)
    GPIO.output(f_pin,GPIO.LOW)
    for i in range(0,10):
        GPIO.output(l_pin,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(l_pin,GPIO.LOW)
        time.sleep(0.05)
    return

def do_everything():
    focus_and_blink(focus_pin,LED_pin)
    take_picture(shutter_pin)
    return







""" START DOING THINGS """


def button_press_detected(switch_pin):
    global button_pressed
    button_pressed = 1
    print('button pressed '+str(button_pressed))

def my_callback(switch_pin):
    focus_and_blink(focus_pin,LED_pin)
    take_picture(shutter_pin)


# Event detection interrupts script when button is pressed
GPIO.add_event_detect(switch_pin,
                      GPIO.RISING,
                      callback=button_press_detected,
                      bouncetime=999
                      )

while 1:
    if button_pressed == 1:
        do_everything()
        print('clicked! '+str(button_pressed))
        button_pressed = 0
    else:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print('\n'+'Goodbye!')
            raise
        print('waiting '+str(button_pressed))





        
