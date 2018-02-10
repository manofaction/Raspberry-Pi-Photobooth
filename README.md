# Python-powered Photobooth

I've been to a number of weddings and other events that have photobooths, and they're always a huge hit.  It's fun to cram into a small space with all your friends, grab a prop, and strike a silly pose - but after all that work guests often walk away with only a small printout of the picture.  Worse, if multiple people are in the shot, only one of them gets to keep it!  I walked away from a lot of shots that would have made great posts on the social media platform of your choice, and I never even got to see any of the pictures that I wasn't actually _in_.

When I got married, I wanted to have a photobooth that had all the fun stuff (i.e. silly props) that encouraged people to take lots of pictures, but I also wanted them to be able to keep those pictures in digital form to use on social media, or print out and frame.  I built a photobooth that uses a DSLR to take high-quality pictures and is controlled by a Raspberry Pi, which coordinates the trigger (a big red button on the floor so guests don't have to move after they get their pose ready), the camera, and a 10" screen.  The photobooth displays the image after taking it, so guests get the immediate satisfaction of seeing their picture, and saves the full-size images to be shared later on social media or printed out.

Here are the steps involved:

1. Guests strike a pose and step on an invitingly large red button on the floor
2. LEDs flash to draw attention to the camera lens
3. Camera takes the picture
4. Picture is displayed on-screen for immediate viewing\
![photobooth](/images/photobooth_with_preview_350x500.jpg)
5. RAW image stays on camera for later retrieval\
 ![photobooth_result](/images/photobooth_example_750x500.jpg)


### Inspiration taken from:

- [Drumminhands](http://www.drumminhands.com/2014/06/15/raspberry-pi-photo-booth/) Raspberry Pi-powered photobooth, which posts to Tumblr
- [alexuadler](https://github.com/alexuadler/drumminhands_photobooth/blob/master/drumminhands_photobooth.py)'s adaptation of same
- [Another Pi-powered photobooth](http://www.instructables.com/id/Raspberry-Pi-photo-booth-controller/?ALLSTEPS) with printer
- [An IDEO employee's photobooth](https://labs.ideo.com/2012/12/14/happy-25th-birthday-gif/) that creates animated GIFs and also features  a big red button
- [This Instructable](http://www.instructables.com/id/DIY-Portable-Wedding-Photo-Booth/?ALLSTEPS) that uses a PVC frame
- [This idea](https://www.engadget.com/2011/06/12/diy-ipad-photo-booth-captures-the-moments-you-might-be-too-drunk/) for fitting all the components into a single box
