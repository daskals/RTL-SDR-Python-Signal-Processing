# RTL-SDR-Python-Signal-Processing
Experimental DSP Python Scripts using an RTL-SDR USB dongle




# Dependencies:
-->Windows/Linux/OSX\
-->Python 2.7.x/3.3+\
-->librtlsdr\
-->Optional: NumPy (wraps samples in a more convenient form)\





# Troubleshooting:

--->Some operating systems (Linux, OS X) seem to result in libusb buffer issues when performing small reads.
Try reading 1024 (or higher powers of two) samples at a time if you have problems.


--->If you’re having librtlsdr import errors:

## Windows:
Make sure all the librtlsdr DLL files (librtlsdr.dll, libusb-1.0.dll) are in your system path, or the same folder as this README file.
Also make sure you have all of their dependencies (e.g. libgcc_s_dw2-1.dll or possibly the Visual Studio runtime files).
If rtl_sdr.exe works, then you should be okay. Also note that you can’t mix the 64 bit version of Python with 32 bit builds of librtlsdr, and vice versa.

in librtlsdr.py replace the following code:

    #driver_files += ['librtlsdr.so', 'rtlsdr/librtlsdr.so']
    #driver_files += ['rtlsdr.dll', 'librtlsdr.so']
    #driver_files += ['..//rtlsdr.dll', '..//librtlsdr.so']
    #driver_files += ['rtlsdr//rtlsdr.dll', 'rtlsdr//librtlsdr.so']
    #driver_files += [lambda : find_library('rtlsdr'), lambda : find_library('librtlsdr')]
    driver_files += ['C:\\your path\\librtlsdr.dll']
    driver_files += ['C:\\your path\\libusb-1.0.dll']
    driver_files += ['C:\\your path\\libwinpthread-1.dll']

## Linux:
Make sure your LD_LIBRARY_PATH environment variable contains the directory where the librtlsdr.so.0 library is located.
You can do this in a shell with (for example): export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib. See this issue for more details.


# Linux RTL SDR Installation:

#!/bin/bash

apt-get update  # update list of available software
apt-get -y install git cmake libusb-1.0-0-dev python python-pip python-dev
apt-get -y install python-scipy python-numpy python-matplotlib


Remove other RTL-SDR driver, if it is loaded
modprobe -r dvb_usb_rtl28xxu

git clone https://github.com/steve-m/librtlsdr
cd librtlsdr
mkdir build
cd build
cmake ../
make
make install
ldconfig

cd

pip install pyrtlsdr

wget https://raw.githubusercontent.com/keenerd/rtl-sdr-misc/master/heatmap/flatten.py

Guide:https://www.rtl-sdr.com/tag/install-guide/

### Troubleshooting:

After installing the libraries you will likely need to unload the DVB-T drivers, which Linux uses by default.
To unload them temporarily type "sudo rmmod dvb_usb_rtl28xxu" into terminal. This solution is only temporary as when you replug the dongle or restart the PC, the DVB-T drivers will be reloaded.
For a permanent solution, create a text file "rtlsdr.conf" in /etc/modprobe.d and add the line "blacklist dvb_usb_rtl28xxu".
You can use the one line command shown below to automatically write and create this file.

echo 'blacklist dvb_usb_rtl28xxu' | sudo tee --append /etc/modprobe.d/blacklist-dvb_usb_rtl28xxu.conf
Now you can restart your device. After it boots up again run "rtl_test" at the terminal with the RTL-SDR plugged in. It should start running.

# Windows RTL SDR Installation:

-->Plug in your dongle. Do not install any of the software that it came with (if any), and ensure that you wait a few seconds for plug and play to finish attempting to install the dongle (it will either fail or install Windows DVB-T TV drivers).
If you've already installed the DVB-T drivers that came on the CD bundled with some dongles, uninstall them first.

-->Install the zadig.exe software . Right click this file and select "Run as administrator".

-->In Zadig, go to "Options->List All Devices" and make sure this option is checked.
If you are using Windows 10, in some cases you may need to also uncheck "Ignore Hubs or Composite Parents".

-->Select "Bulk-In, Interface (Interface 0)" from the drop down list.
Note on some PCs you may see something like RTL2832UHIDIR or RTL2832U instead of the bulk in interface.
This is also a valid selection.
Do not select "USB Receiver (Interface 0) or Interface 1" or anything else or you will overwrite that driver!
Double check that USB ID shows "0BDA 2838 00" as this indicates that the dongle is selected.

-->We need to install the WinUSB driver, so also ensure that WinUSB is selected in the box after the arrow next to where it says Driver (this is the default selection)

-->Click Replace Driver. On some PC's you might get a warning that the publisher cannot be verified, but just accept it by clicking on "Install this driver software anyway".
This will install the drivers necessary to run the dongle as a software defined radio.
Note that you may need to run zadig.exe again if you move the dongle to another USB port, or want to use two or more dongles together.