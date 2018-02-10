
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
import config
from signal import alarm, signal, SIGALRM, SIGKILL
import subprocess
from subprocess import call
import commands
from threading import Thread

##### Config Variables #####
led1_pin = 12 # LED 1
led2_pin = 16 # LED 2
led3_pin = 20 # LED 3
led4_pin = 21 # LED 4
button1_pin = 18 # pin for the big red button
button2_pin = 22 # pin for button to shutdown the pi
button3_pin = 17 # pin for button to end the program, but not shutdown the pibutton1_pin = 18
button4_pin = 27 # pin for the print button

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
backg_fill = 255,255,255


replay_delay = 1 # how much to wait in-between showing pics on-screen after taking
replay_cycles = 2 # how many times to show each photo on-screen after takingtransform

test_server = 'www.google.com'
real_path = os.path.dirname(os.path.realpath(__file__))

##### Config GPIO Parameters #####
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1_pin,GPIO.OUT) # LED 1
GPIO.setup(led2_pin,GPIO.OUT) # LED 2
GPIO.setup(led3_pin,GPIO.OUT) # LED 3
GPIO.setup(led4_pin,GPIO.OUT) # LED 4
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection on button 1
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection on button 2
GPIO.setup(button3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection on button 3
GPIO.setup(button4_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection on button 4
GPIO.output(led1_pin,False);
GPIO.output(led2_pin,False);
GPIO.output(led3_pin,False);
GPIO.output(led4_pin,False); #for some reason the pin turns on at the beginning of the program. why?????????????????????????????????

#################
### Functions ###
#################

def cleanup():
  print('Ended abruptly')
  GPIO.cleanup()
atexit.register(cleanup)

def shut_it_down(channel):  
    print "Shutting down..." 
    GPIO.output(led1_pin,True);
    GPIO.output(led2_pin,True);
    GPIO.output(led3_pin,True);
    GPIO.output(led4_pin,True);
    time.sleep(3)
    os.system("sudo halt")

def exit_photobooth(channel):
#    global actuations
#    global print_count
    print "Photo booth app ended. RPi still running" 
    GPIO.output(led1_pin,True);
    time.sleep(3)
#    print "Took: " + actuations + " photos"
#    print "Printed " + print_count + " mementos"
    sys.exit()
    
def clear_pics(foo): #why is this function being passed an arguments?
    #delete files in folder on startup
	files = glob.glob(config.file_path + '*')
	for f in files:
		os.remove(f) 
	#light the lights in series to show completed
	print "Deleted previous pics"
	GPIO.output(led1_pin,False); #turn off the lights
	GPIO.output(led2_pin,False);
	GPIO.output(led3_pin,False);
	GPIO.output(led4_pin,False)
	pins = [led1_pin, led2_pin, led3_pin, led4_pin]
	for p in pins:
		GPIO.output(p,True); 
		sleep(0.25)
		GPIO.output(p,False);
		sleep(0.25)
   
def init_pygame():
    pygame.init()
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    pygame.display.set_caption('Photo Booth Pics')
    #pygame.display.set_mode(size).fill(backg_fill)
    pygame.mouse.set_visible(False) #hide the mouse cursor
    return pygame.display.set_mode(size, pygame.FULLSCREEN)

def capture_image(namescheme):
    call ("gphoto2 --capture-image-and-download --filename=" +
          config.file_path +
          namescheme + ".%C", shell=True)

def backup_raw(namescheme):
    call("mv "+config.file_path +
         namescheme+ ".nef " +
         config.raw_path + namescheme + ".nef", shell=True)

def show_image(image_path):
    screen = init_pygame()
    screen.fill(backg_fill)
    img=pygame.image.load(image_path) 
    img = pygame.transform.scale(img,(transform_x,transfrom_y))
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()

def display_pics(jpg_group):
    # this section is an unbelievable nasty hack - for some reason Pygame
    # needs a keyboardinterrupt to initialise in some limited circs (second time running)

    class Alarm(Exception):
        pass
    def alarm_handler(signum, frame):
        raise Alarm
    signal(SIGALRM, alarm_handler)
    alarm(3)
    try:
        screen = init_pygame()

        alarm(0)
    except Alarm:
        raise KeyboardInterrupt
    filename = config.file_path + jpg_group + ".jpg"
    show_image(filename)

def print_pic(namescheme):
    call ("lp -d Canon_CP800 " +
          config.file_path +
          namescheme + ".jpg", shell=True)
    call ("lpr", shell = True)

def check_for_print():
  timeout = time.time() + show_pic_delay
  global print_choice
#  global print_count
  while time.time() < timeout:
    if GPIO.input(button4_pin)==0:
          print_choice = 1
#          print_count += 1
  if print_choice==1:
    GPIO.output(led3_pin, True)
    time.sleep(2)
    GPIO.output(led3_pin, False)
    print "Sending picture to printer"
  else:
    GPIO.output(led4_pin, True)
    time.sleep(2)
    GPIO.output(led4_pin, False)
    print "Continuing without printing"


# define the photo taking function for when the big button is pressed 
def start_photobooth(): 
#        global actuations

	################################# Begin Step 1 ################################# 
	show_image(real_path + "/blank.png")
	print "Get Ready"
	GPIO.output(led1_pin,True);
	show_image(real_path + "/our_cues/get_ready.png")
	sleep(prep_delay) 
	GPIO.output(led1_pin,False)

###### Need to insert a "look at the camera" cue
#	show_image(real_path + "/blank.png")

# This is where I would initialize the parameters for Gphoto2 and the preview. For now, I'm leaving it out.
	
	sleep(2) #warm up camera

	################################# Begin Step 2 #################################
	print "Taking pics"
	
	now = time.strftime("%Y-%m-%d-%H:%M:%S") #need to let python decide file name so I can reference it

        capture_image(now)
#        actuations += 1 
        backup_raw(now)

	########################### Begin Step 3 #################################
#        print "Postprocessing" 
#	if post_online:
#		show_image(real_path + "/uploading.png")
#	else:
#		show_image(real_path + "/processing.png")

#	GPIO.output(led3_pin,True) #turn on the LED
#	print "Uploading to tumblr. Please check " + config.tumblr_blog + ".tumblr.com soon."

#	if post_online: # turn off posting pics online in the variable declarations at the top of this document
#		connected = is_connected() #check to see if you have an internet connection
#		while connected: 
#			try:
#				file_to_upload = config.file_path + now + ".gif"
#				client.create_photo(config.tumblr_blog, state="published", tags=["drumminhandsPhotoBooth"], data=file_to_upload)
#				break
#			except ValueError:
#				print "Oops. No internect connection. Upload later."
#				try: #make a text file as a note to upload the .gif later
#					file = open(config.file_path + now + "-FILENOTUPLOADED.txt",'w')   # Trying to create a new file or open one
#					file.close()
#				except:
#					print('Something went wrong. Could not write file.')
#					sys.exit(0) # quit Python
#	GPIO.output(led3_pin,False) #turn off the LED
	
	########################### Begin Step 4 #################################
	GPIO.output(led4_pin,True) #turn on the LED
        print_response = None
	try:
		display_pics(now)
	except Exception, e:
		tb = sys.exc_info()[2]
		traceback.print_exception(e.__class__, e, tb)
	#pygame.quit()
	print "Done"

        print_choice = 0
        timeout = time.time() + show_pic_delay
        while time.time() < timeout:
          if GPIO.input(button4_pin)==0:
            print_choice = 1
        if print_choice==1:
          GPIO.output(led3_pin, True)
          time.sleep(2)
          GPIO.output(led3_pin, False)
          print "Sending picture to printer"
        else:
          GPIO.output(led4_pin, True)
          time.sleep(2)
          GPIO.output(led4_pin, False)
          print "Continuing without printing"

	GPIO.output(led4_pin,False) #turn off the LED
	
	if print_choice == 1:
		show_image(real_path + "/processing.png")
		print_pic(now)
	else:
		show_image(real_path + "/our_cues/finished.png")
	
	time.sleep(restart_delay)
	show_image(real_path + "/our_cues/intro.png");



####################
### Main Program ###
####################

# when a falling edge is detected on button2_pin and button3_pin, regardless of whatever   
# else is happening in the program, their function will be run   
GPIO.add_event_detect(button2_pin, GPIO.FALLING, callback=shut_it_down, bouncetime=300) 

#choose one of the two following lines to be un-commented
GPIO.add_event_detect(button3_pin, GPIO.FALLING, callback=exit_photobooth, bouncetime=300) #use third button to exit python. Good while developing
#GPIO.add_event_detect(button3_pin, GPIO.FALLING, callback=clear_pics, bouncetime=300) #use the third button to clear pics stored on the SD card from previous events

# delete files in folder on startup
files = glob.glob(config.file_path + '*')
for f in files:
    os.remove(f)

print "Photo booth app running..." 
GPIO.output(led1_pin,True); #light up the lights to show the app is running
GPIO.output(led2_pin,True);
GPIO.output(led3_pin,True);
GPIO.output(led4_pin,True);
time.sleep(3)
GPIO.output(led1_pin,False); #turn off the lights
GPIO.output(led2_pin,False);
GPIO.output(led3_pin,False);
GPIO.output(led4_pin,False);

show_image(real_path + "/our_cues/intro.png");
# actuations = 0
# print_count = 0
while True:
        GPIO.wait_for_edge(button1_pin, GPIO.FALLING)
        print "start button pressed"
	time.sleep(0.2) #debounce
	start_photobooth()
Contact GitHub API Training Shop Blog About
© 2016 GitHub, Inc. Terms Privacy Security Status Help
