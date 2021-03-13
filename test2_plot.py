#######################################################
#     Spiros Daskalakis                               #
#     Last Revision: 13/03/2021                       #
#     Python Version:  3.9                            #
#     Email: Daskalakispiros@gmail.com                #
#######################################################

from rtlsdr import RtlSdr
from matplotlib import pyplot as plt

sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.048e6  # Hz
sdr.center_freq = 98e6  # Hz
sdr.freq_correction = 60  # PPM
sdr.gain = 'auto'
samples = sdr.read_samples(256 * 1024)
sdr.close()

# use matplotlib to estimate and plot the PSD
plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate / 1e6, Fc=sdr.center_freq / 1e6)
plt.xlabel('Frequency (MHz)')
plt.ylabel('Relative power (dB)')
plt.show()



