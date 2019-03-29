# cranegui

In order to use Tkinter within python 2 run ```sudo apt-get install python-tkinter```

Dependencies for Labjack

Files Needed:

LabJackPython-2.0.0 [link for python module](https://labjack.com/support/software/examples/ud/labjackpython)

  -python module for labjack so we can import u6 and use it to interface with the labjack.
  
exodriver-master [link for exodriver](https://labjack.com/support/software/installers/ud)

  -linux drivers for the labjack, which needs libusb. I downloaded libusb and libusb-devel from package manager as a    dependency.
  documention to install exodriver [here](https://labjack.com/support/software/installers/exodriver).
  
  ```sudo apt-get install libusb-1.0-0-dev```
  
  ```pip install Pillow (PIL, image processing)```
  
  ```pip install numpy```
  
  check for usb devices: ```python -m evdev.evtest```
  
  let all use event in device folder
  
  ```chmod a+rw /dev/input/event19```

  In order to get auto boot after gui starts:

  Navigate to /etc/xdg/lxsession/LXDE-pi/autostart

  Add "@/usr/bin/python /home/pi/code/guitest.py" to the last line of the file.

  Also since the script is pulling .png files from the images folder, the folder
  needs to be put into the home directory (/home/pi/) since the script is being
  run from there as well.
