#######################################################
#     Spiros Daskalakis                               #
#     Last Revision: 13/03/2021                       #
#     Python Version:  3.9                            #
#     Email: Daskalakispiros@gmail.com                #
#######################################################
from rtlsdr import RtlSdr

sdr = RtlSdr()

# configure RTL sdr  device
sdr.sample_rate = 2.048e6  # Hz
sdr.center_freq = 100e6    # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

print(sdr.read_samples(512))