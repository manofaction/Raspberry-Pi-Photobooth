

""" SETUP  """
import os
#import glob
import time
#import traceback
import RPi.GPIO as GPIO
#import atexit
#import sys
#import socket
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from signal import alarm, signal, SIGALRM, SIGKILL
import subprocess
from subprocess import call
#import commands
#from threading import Thread
import pandas as pd
import StringIO

LED_pin = 11
switch_pin = 16
focus_pin = 22
shutter_pin = 12

monitor_w = 1280
monitor_h = 800
transform_x = 1200 # how wide to scale the jpg when replaying
transform_y = 800 # how high to scale the jpg when replaying
offset_x = 50 # how far off to left corner to display photos
offset_y = 0 # how far off to left corner to display photos
backg_fill = 0,0,0

camera_did_not_trigger_filename = "/home/pi/Documents/Python-Photobooth/images/camera_did_not_trigger.png"
processing_filename = "/home/pi/Documents/Python-Photobooth/images/processing.png"
image_directory = "/home/pi/Documents/photobooth_pics/"

# A function to handle keyboard/mouse/device input events    
def input(events):
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == pygame.QUIT or
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            pygame.quit()
   
def init_pygame():
    pygame.init()
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    pygame.display.set_mode(size).fill(backg_fill)
    pygame.mouse.set_visible(False) # Hides the mouse cursor
    return pygame.display.set_mode(size, pygame.FULLSCREEN)
    #return pygame.display.set_mode(size, pygame.RESIZABLE)

def get_image_filename(image_directory):
    image_filename = image_directory + "photobooth_" + time.strftime("%Y-%m-%d-%H-%M-%S")
    return (image_filename)

def list_files():
    p = subprocess.Popen(['gphoto2', '--list-files'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = p.communicate()[0]
    return result

def get_filenumber(file_list):
    # Note:  This breaks if your SD card reaches img_9999 and starts over at img_0001 in the middle of the wedding reception.
    # TO DO: Regex currently grabs ALL numeric characters, even the 2 in ".CR2"
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
    return(high_filenumber)

def get_file(filenumber, image_filename):
    call ('gphoto2 ' +
          '--get-file ' +
          '%s ' % filenumber +
          '--filename ' +
          '%s' % image_filename,
          shell=True)

def show_image(image_filename):
    screen.fill(backg_fill)
    img = pygame.image.load(image_filename) 
    img = pygame.transform.scale(img, (transform_x, transform_y))
    screen.blit(img, (offset_x, offset_y))
    pygame.display.flip()

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

def focus_and_blink(f_pin, l_pin):
    GPIO.output(f_pin, GPIO.HIGH)
    for i in range(0, 4):
        GPIO.output(l_pin, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(l_pin, GPIO.LOW)
        time.sleep(0.25)
    GPIO.output(f_pin, GPIO.LOW)
    for i in range(0, 10):
        GPIO.output(l_pin, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(l_pin, GPIO.LOW)
        time.sleep(0.05)
    return

def take_picture(pin):
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin,GPIO.LOW)
    
def check_for_updated_filenumber(original_filenumber, timeout_limit = 3):
    time_end = time.time() + timeout_limit
    while time.time() < time_end:
        file_list = list_files()
        filenumber = get_filenumber(file_list)
        if filenumber != original_filenumber:
            return filenumber
    return original_filenumber

def test_if_real_button_press():
    time.sleep(0.05)
    if GPIO.input(switch_pin) != GPIO.LOW:
        return False
    else if GPIO.input(switch_pin) == GPIO.LOW:
        return True

def start_photobooth():
    
    if test_if_real_button_press() == False:
        return

    screen.fill(backg_fill)
    pygame.display.update()
    
    file_list = list_files()
    original_filenumber = get_filenumber(file_list)    

    time.sleep(0.25)

    focus_and_blink(focus_pin,LED_pin)
    take_picture(shutter_pin)

    show_image(processing_filename)

    filenumber = check_for_updated_filenumber(original_filenumber)

    if filenumber == original_filenumber:
        show_image(camera_did_not_trigger_filename)
    else:
        image_filename = get_image_filename(image_directory)
    
        try:
            get_file(filenumber, image_filename)
        except pygame.error:
            show_image(camera_did_not_trigger_filename)
        
        show_image(image_filename)

        
""" START DOING THINGS """

# use RPi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set up GPIO output channel
GPIO.setup(LED_pin,GPIO.OUT)
GPIO.setup(focus_pin,GPIO.OUT)
GPIO.setup(shutter_pin,GPIO.OUT)

# set up switch
GPIO.setup(switch_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# initialize pygame
pygame.init()
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
#pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
screen = pygame.display.get_surface()

while True:
    input(pygame.event.get())
    GPIO.wait_for_edge(switch_pin, GPIO.RISING)
    start_photobooth()

















