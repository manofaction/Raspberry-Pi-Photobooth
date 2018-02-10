
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
# import config
from signal import alarm, signal, SIGALRM, SIGKILL
import subprocess
from subprocess import call
import commands
from threading import Thread


post_online = 0
total_pics = 1
capture_delay = 2
prep_delay = 3
show_pic_delay = 6
restart_delay = 3
enable_printing = 1

monitor_w = 1280
monitor_h = 800
transform_x = 1200 # how wide to scale the jpg when replaying
transfrom_y = 800 # how high to scale the jpg when replaying
offset_x = 40 # how far off to left corner to display photos
offset_y = 0 # how far off to left corner to display photos
backg_fill = 0,0,0


replay_delay = 1 # how much to wait in-between showing pics on-screen after taking
replay_cycles = 2 # how many times to show each photo on-screen after takingtransform

test_server = 'www.google.com'
real_path = os.path.dirname(os.path.realpath(__file__))



def exit_photobooth(channel):
#    global actuations
#    global print_count
    print "Photo booth app ended. RPi still running" 
    GPIO.output(led1_pin,True);
    time.sleep(3)
#    print "Took: " + actuations + " photos"
#    print "Printed " + print_count + " mementos"
    sys.exit()

   
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

image_directory = "/home/pi/Documents/Python-Photobooth/images/"

filename = "picture_2.jpg"

print("About to start working")
sleep(1)
show_image(image_directory + filename)
sleep(15)
    
