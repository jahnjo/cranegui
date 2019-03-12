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
  
  check for usb devices: ```python -m evdev.evtest```
  
  let all use event in device folder
  
  ```chmod a+rw /dev/input/event19```
