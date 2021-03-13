#######################################################
#     Spiros Daskalakis                               #
#     Last Revision: 13/03/2021                       #
#     Python Version:  3.9                            #
#     Email: Daskalakispiros@gmail.com                #
#######################################################

import asyncio

import numpy as np
from rtlsdr import RtlSdr
from matplotlib import pyplot as plt
import scipy.signal as sps

def CFO_pilot_tone(analog_signal, F_s):
    x_R_fft = np.fft.fftshift(np.fft.fft(analog_signal))
    LPF = np.zeros(x_R_fft.size)  # create
    N_F = x_R_fft.size
    F_axis = np.arange(-F_s / 2, F_s / 2, F_s / N_F)
    LPF[(np.abs(F_axis) >= 15100) & (np.abs(F_axis) <= 23300)] = 1
    x_R_filt_fft = x_R_fft * LPF  # filter in freq domain
    mpos = np.argmax(np.abs(x_R_filt_fft))
    # Shift the signal based on the 19 KHz carrier
    DF_est = np.abs(19000 + F_axis[mpos])
    print(DF_est)
    if np.abs(F_axis[mpos]) > 19000:
        pack = np.exp(-1.0j * 2.0 * np.pi * DF_est / F_s * np.arange(len(analog_signal)))
        analog_signal = analog_signal * pack
    elif np.abs(F_axis[mpos]) < 19000:
        pack = np.exp(+1.0j * 2.0 * np.pi * DF_est / F_s * np.arange(len(analog_signal)))
        analog_signal = analog_signal * pack
    return analog_signal


async def streaming():
    sdr = RtlSdr()
    # configure device
    # Fs = 2.4e6   # Hz
    Fs = 1e6
    sdr.sample_rate = Fs  # Hz
    sdr.center_freq = 95.8e6  # Hz
    sdr.freq_correction = 60  # PPM
    sdr.gain = 'auto'
    # Sampling for 1 sec
    t_sampling = 0.1
    N_samples = round(Fs * t_sampling)
    samples = sdr.read_samples(N_samples)
    CFO_corr_en = 0

    fig = plt.figure(1)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Relative power (dB)')
    fig.show()

    LEFT = 15000
    BW = 8000
    F_center = LEFT + BW / 2

    async for samples in sdr.stream():

        # Convert samples to a numpy array
        x1 = np.array(samples).astype("complex64")

        if CFO_corr_en == 1:
            analog_signal_packets = CFO_pilot_tone(x1, Fs)
        else:
            analog_signal_packets = x1

        # To mix the data down, generate a digital complex exponential
        # (with the same length as x1) with phase -F_offset/Fs
        fc1 = np.exp(-1.0j * 2.0 * np.pi * F_center / Fs * np.arange(len(analog_signal_packets)))
        # Now, just multiply x1 and the digital complex exponential
        x2 = analog_signal_packets * fc1

        # channelize the signal Method 1
        ########################################################################
        newrate = BW
        samples = round(x2.size * newrate / Fs)
        resampled_signal1 = sps.resample(x2, samples)
        ########################################################################
        # channelize the signal Method 2
        ########################################################################
        # Find a decimation rate to achieve audio sampling rate between 44-48 kHz
        audio_freq = 44100.0
        dec_audio = round(Fs / audio_freq)
        resampled_signal2 = sps.decimate(x2, dec_audio)
        Fs_audio = Fs / dec_audio
        ########################################################################

        plt.psd(resampled_signal2, NFFT=1024, Fs=Fs_audio, Fc=sdr.center_freq / 1e6)
        plt.title("Dynamic Plot")
        plt.draw()
        plt.pause(0.1)
        fig.clear()

    # to stop streaming:
    await sdr.stop()

    # done
    sdr.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(streaming())
