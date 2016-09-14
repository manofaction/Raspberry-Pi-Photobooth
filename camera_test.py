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
from subprocess import call, Popen, PIPE
import commands
import time
import re
import pandas as pd
import StringIO

filenumber = '965'



def list_files():
    #call ("gphoto2 " +
    #      "--list-files",
    #      shell=True)
    import subprocess
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
    return(high_filenumber)

def checknum():
    call ("gphoto2 " +
          "--folder " +
          "/store_00020001/DCIM/101CANON " +
          "--num-files",
          shell=True)

def capture_image():
    call ("gphoto2 " +
          "--capture-image",
          shell=True)

def get_file():

    filename = "photobooth_" + time.strftime("%Y-%m-%d-%H-%M-%S")
    
    call ('gphoto2 ' +
          '--get-file ' +
          '%s ' % filenumber +
          '--filename ' +
          '%s' % filename,
          shell=True)




#capture_image()
#checknum()
#get_file()
file_list = list_files()
filenumber = get_filenumber(file_list)
print(filenumber)

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

##each_line = file_list.split('\n')
##jpeg_pattern = re.compile('*JPG')
##
##for m in each_line:
##    n = re.search('JPG', each_line)
##    print n
