import numpy as np
import wave
import matplotlib.pyplot as plt

MS_TO_S = 1000
EPSILON = 1e-4

# difference function
def DF(time_series, window, lag):
    return np.sum(np.square(time_series[lag:lag+window]
            - time_series[:window]))

# get number of samples from time length and sample rate
def num_samples(time, sample_rate=44100):
    return int(sample_rate * (time / MS_TO_S))

def find_pitch(time_series, sample_rate=44100, window_time=30, max_lag_time=50, thresh=0.1, bad_input_thresh=0.15):
    # set window width and maximum lag to test
    window = num_samples(window_time, sample_rate)
    max_lag = min(num_samples(max_lag_time, sample_rate), len(time_series) - window)

    if window > len(time_series):
        return None

    # normalize time_series
    mean = np.mean(time_series[:window])
    std = np.std(time_series[:window])
    if mean < EPSILON and std < EPSILON:
        return None
    time_series = (time_series - mean) / (std)

    under_thresh = False
    cumulative_df = 0 # cumulative sum of difference function
    min_cmndf = 1 # min value of cumulative mean normalized difference function
    min_cmndf_index = 1 # index for above
    for lag in range(1, max_lag):
        squared_difference = DF(time_series, window, lag)
        cumulative_df += squared_difference
        cmndf = squared_difference / (cumulative_df / lag)

        if cmndf < min_cmndf:
            min_cmndf = cmndf
            min_cmndf_index = lag

        if cmndf < thresh: # first value seen below threshold
            under_thresh = True
        elif under_thresh: # break loop once above threshold
            break

    if min_cmndf > bad_input_thresh:
        return None
    else:
        return 1 / (min_cmndf_index / sample_rate)

