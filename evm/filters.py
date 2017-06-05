import numpy as np
import scipy.fftpack as fftpack 

def temporal_bandpass_filter(data, fps, freq_min=0.833, freq_max=1, axis=0, amplification_factor=1):
    """Found from https://github.com/brycedrennan/eulerian-magnification. Will expand later."""
    fft = fftpack.rfft(data, axis=axis)
    frequencies = fftpack.fftfreq(data.shape[0], d=1.0 / fps)
    bound_low = (np.abs(frequencies - freq_min)).argmin()
    bound_high = (np.abs(frequencies - freq_max)).argmin()
    fft[:bound_low] = 0
    fft[bound_high:-bound_high] = 0
    fft[-bound_low:] = 0

    result = np.ndarray(shape=data.shape, dtype='float')
    result[:] = fftpack.ifft(fft, axis=0)
    result *= amplification_factor
    return result
