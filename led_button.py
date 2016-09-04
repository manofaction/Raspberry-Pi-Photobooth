# Listen for a press from momentary switch (GPIO-23 / pin 16 - GND), then:
# Blink an LED connected from GPIO 17 (pin 11) to ground (pin 6)

""" SETUP  """
import os
import glob
import time
import traceback
from time import sleep
import RPi.GPIO as GPIO
import atexit
import sys
import socket
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
# import config
from signal import alarm, signal, SIGALRM, SIGKILL
import subprocess
from subprocess import call
import commands
from threading import Thread
import time

LED_pin = 11
switch_pin = 16
image_directory = "/home/pi/Documents/photobooth_pics/"

filename = "picture_2.jpg"

monitor_w = 1280
monitor_h = 800
transform_x = 1200 # how wide to scale the jpg when replaying
transfrom_y = 800 # how high to scale the jpg when replaying
offset_x = 40 # how far off to left corner to display photos
offset_y = 0 # how far off to left corner to display photos
backg_fill = 0,0,0


# A function to handle keyboard/mouse/device input events    
def input(events):
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()
                
   
def init_pygame():
    pygame.init()
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    pygame.display.set_caption('Photo Booth Pics')
    #pygame.display.set_mode(size).fill(backg_fill)
    pygame.mouse.set_visible(False) #hide the mouse cursor
    return pygame.display.set_mode(size, pygame.FULLSCREEN)


def show_image(image_path):
    screen = init_pygame()
    screen.fill(backg_fill)
    img=pygame.image.load(image_path) 
    img = pygame.transform.scale(img,(transform_x,transfrom_y))
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()



# initialize pygame
pygame.init()
modes = pygame.display.list_modes()
pygame.display.set_mode(max(modes))
screen = pygame.display.get_surface()
pygame.display.set_caption('Photo Booth Pics')
pygame.mouse.set_visible(False) #hide the mouse cursor
pygame.display.toggle_fullscreen()

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
    
#def my_callback(channel):
def start_photobooth():
    screen.fill( (0,0,0) )
    pygame.display.update()
    
    blink(LED_pin)
    take_picture()

    show_image(image_directory + filename)

""" START DOING THINGS """

# run the blink function
##
##GPIO.add_event_detect(switch_pin,
##                      GPIO.RISING,
##                      callback=my_callback,
##                      bouncetime=999
##                      )
##
##try:
##    time.sleep(100)
##except KeyboardInterrupt:
##    GPIO.cleanup()
##    print('See ya!')
##
##   
##GPIO.cleanup()

while True:
    input(pygame.event.get())
    GPIO.wait_for_edge(switch_pin, GPIO.RISING)
    time.sleep(1)
    start_photobooth()

















