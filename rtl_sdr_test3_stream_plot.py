#######################################################
#     Spiros Daskalakis                               #
#     Last Revision: 09/03/2021                       #
#     Python Version:  3.9                            #
#     Email: Daskalakispiros@gmail.com                #
#######################################################

import asyncio
from rtlsdr import RtlSdr
from matplotlib import pyplot as plt

async def streaming():
    sdr = RtlSdr()
    # configure device
    Fs = 2.4e6   # Hz
    sdr.sample_rate = Fs  # Hz
    sdr.center_freq = 98e6  # Hz
    sdr.freq_correction = 60  # PPM
    sdr.gain = 'auto'

    t_sampling = 1  # Sampling
    N_samples = round(Fs * t_sampling)

    samples = sdr.read_samples(N_samples)

    fig = plt.figure(1)

    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Relative power (dB)')
    fig.show()

    async for samples in sdr.stream():
        # do something with samples
        plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate / 1e6, Fc=sdr.center_freq / 1e6)
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
