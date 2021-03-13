#######################################################
#     Spiros Daskalakis                               #
#     Last Revision: 09/03/2021                       #
#     Python Version:  3.9                            #
#     Email: Daskalakispiros@gmail.com                #
#######################################################

from rtlsdr import RtlSdr
from matplotlib import pyplot as plt
import numpy as np


def find_powerfull_FM():
    sdr = RtlSdr()
    # configure device
    Fs = 2e6  # Hz
    sdr.sample_rate = Fs  # Hz
    sdr.freq_correction = 60  # PPM
    sdr.gain = 'auto'

    FM_band_min = 87.5
    FM_band_max = 109

    powe = np.ndarray(0)
    freq = np.ndarray(0)

    t_sampling = 0.1  # Sampling for 100 ms
    N_samples = round(Fs * t_sampling)

    for i in np.arange(FM_band_min, FM_band_max, Fs / 1e6):
        sdr.center_freq = i * 1e6  # Hz
        counter = 0
        prev_int = 0
        while 1:
            counter = counter + 1
            samples = sdr.read_samples(N_samples)
            ###################################################################################
            power, psd_freq = plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate / 1e6, Fc=sdr.center_freq / 1e6)
            #####################################################################################
            ind_pow = np.argmax(power)
            freq_ind = round(psd_freq[ind_pow], 1)
            if freq_ind == prev_int and counter >= 3:
                powe = np.append(powe, ind_pow)
                freq = np.append(freq, freq_ind)
                break
            prev_int = freq_ind
    # done
    sdr.close()
    max_fm_station_power = np.argmax(powe)
    max_fm_station_freq = freq[max_fm_station_power]
    return max_fm_station_freq

print('FM with max Power is (MHz):', find_powerfull_FM())
