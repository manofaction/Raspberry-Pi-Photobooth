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
import subprocess
from subprocess import call
import commands
import pandas as pd
import StringIO

LED_pin = 11
switch_pin = 16
focus_pin = 22
shutter_pin = 12

image_directory = "/home/pi/Documents/photobooth_pics/"
image_filename = "WRONG_FILENAME"
#filenumber = '965'

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
        if (event.type == pygame.QUIT or
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            pygame.quit()
                
   
def init_pygame():
    pygame.init()
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    pygame.display.set_caption('Photo Booth Pics')
    #pygame.display.set_mode(size).fill(backg_fill)
    pygame.mouse.set_visible(False) #hide the mouse cursor
    #return pygame.display.set_mode(size, pygame.FULLSCREEN)
    return pygame.display.set_mode(size, pygame.RESIZABLE)

def get_image_filename(image_directory):
    image_filename = image_directory + "photobooth_" + time.strftime("%Y-%m-%d-%H-%M-%S")
    return (image_filename)

def list_files():
    p = subprocess.Popen(['gphoto2', '--list-files'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = p.communicate()[0]
    return result

def get_filenumber(file_list):
        
    df = pd.read_csv(StringIO.StringIO(file_list),
                       header=None,
                       comment='T',
                       sep=r'\s*',
                       names=['file_number', 'img_number', 'rd_col', 'file_size', 'kb_col', 'file_type'],
                       usecols=['file_number', 'img_number', 'file_type'],
                       engine='python')

    df = df.dropna(how='any')
    df = df[df.file_type == 'image/jpeg']
    df.file_number = df.file_number.str[1:]
    df.file_number = df.file_number.convert_objects(convert_numeric=True)
    df.img_number = df.img_number.str.replace('[^0-9]', '').astype(float)
    high_filenumber = df.file_number[df.img_number.idxmax()]
    #print(high_filenumber)

    #high_filenumber = int(high_filenumber) + 2
    #print(high_filenumber)
    return(high_filenumber)

def get_file(filenumber, image_filename):
    call ('gphoto2 ' +
          '--get-file ' +
          '%s ' % filenumber +
          '--filename ' +
          '%s' % image_filename,
          shell=True)

def show_image(image_filename):
    screen = init_pygame()
    screen.fill(backg_fill)
    img=pygame.image.load(image_filename) 
    img = pygame.transform.scale(img,(transform_x,transfrom_y))
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()



# initialize pygame
pygame.init()
#modes = pygame.display.list_modes()
#pygame.display.set_mode(max(modes))
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
pygame.display.set_mode(size, pygame.RESIZABLE)
screen = pygame.display.get_surface()
pygame.display.set_caption('Photo Booth Pics')
#pygame.mouse.set_visible(False) #hide the mouse cursor
#pygame.display.toggle_fullscreen()

# use RPi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set up GPIO output channel
GPIO.setup(LED_pin,GPIO.OUT)
GPIO.setup(focus_pin,GPIO.OUT)
GPIO.setup(shutter_pin,GPIO.OUT)

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

def take_picture(pin):
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin,GPIO.LOW)

##    call ('gphoto2 ' +
##          '--capture-image',
##          shell=True)
##    return

def start_photobooth():
    screen.fill( (0,0,0) )
    pygame.display.update()
    time.sleep(0.25)

    focus_and_blink(focus_pin,LED_pin)
    take_picture(shutter_pin)
    
    time.sleep(0.05)
    
    file_list = list_files()
    filenumber = get_filenumber(file_list)
    
    image_filename = get_image_filename(image_directory)
    get_file(filenumber, image_filename)

    show_image(image_filename)

""" START DOING THINGS """

while True:
    input(pygame.event.get())
    GPIO.wait_for_edge(switch_pin, GPIO.RISING)
    start_photobooth()

















