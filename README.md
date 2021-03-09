# RTL-SDR-Python-Signal-Processing
Experimental DSP Python Scripts using an RTL-SDR USB dongle


## Driver Installation

# Windows:


## Troubleshooting

--->Some operating systems (Linux, OS X) seem to result in libusb buffer issues when performing small reads.
Try reading 1024 (or higher powers of two) samples at a time if you have problems.


--->If you’re having librtlsdr import errors:
# Windows:
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



# Linux:
Make sure your LD_LIBRARY_PATH environment variable contains the directory where the librtlsdr.so.0 library is located.
You can do this in a shell with (for example): export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib. See this issue for more details.



