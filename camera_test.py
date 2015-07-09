"""
Control camera from Pi using gphoto2

Notes:
    -If I encounter again the problem where the cam takes one pic but then
     doesn't respond to the second, try adding sudo, i.e. "sudo gphoto2",...
    -Actually I think the problem was I needed to update gphoto2 to the
     newest version.  It seems to work repeatedly now.

"""
from PIL import Image
import subprocess
from subprocess import call
import commands

filenumber = '1120'

def list_files():
    call ("gphoto2 " +
          "--list-files",
          shell=True)

def checknum():
    call ("gphoto2 " +
          "--folder " +
          "/store_00020001/DCIM/100CANON " +
          "--num-files",
          shell=True)

def capture_image():
    call ("gphoto2 " +
          "--capture-image",
          shell=True)

def get_file():
    call ('gphoto2 ' +
          '--get-file ' +
          '%s ' % filenumber +
          '--filename ' +
          'whatever2.jpg',
          shell=True)




capture_image()
checknum()
#get_file()
#list_files()

'''
#output = subprocess.Popen([checknum()], stdout=subprocess.PIPE).communicate()[0]

#print commands.getstatusoutput(checknum())

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    #return iter(p.stdout.readline, b'')
    out, err = p.communicate()
    print out


p = subprocess.Popen('call (["gphoto2","--folder","/store_00020001/DCIM/100CANON","--num-files"])',
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    #return iter(p.stdout.readline, b'')
out, err = p.communicate()
print out

'''
    
"""

HOW TO DOWNLOAD ONLY JPEG:
gphoto2 --list-files    # Lists files on camera and numbers each of them.
                        # The most recent JPG is the highest number.
                        # Most recent CR2 is second highest.
gphoto2 --get-file 1533 # Downloads ONLY file no. 1533 (whatever the last # is)

gphoto2 --get-file 1533 --filename whatever.jpg

# Following line checks number of files on camera!  How do I save the output?
gphoto2 --folder /store_00020001/DCIM/100CANON --num-files



After each time you take a picture, just increment the file no. by 2!

gphoto2 --folder 

#call (["gphoto2","--capture-image-and-download"])
       
# LINE BELOW: How to specify file name - but how does that work with saving
#             both jpg AND cr2 files?
#call (["gphoto2","--capture-image-and-download",
#       "--filename","/home/pi/camera/photo-%Y%m%d-%H%M%S.jpg"

#root = Tkinter.Tk()
#root.geometry('+%d+%d', % (50,50))

#img = Image.open("capt0000.jpg")
#photo = ImageTk.PhotoImage(img)


"""
