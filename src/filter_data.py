import scipy.signal as signal
import numpy as np
import pandas as pd

def filter_data(filename):
    # Replace 'your_data.csv' with your actual filename
    data = pd.read_csv(filename)

    # Columns start with channel 1
    channels = data.columns[1:]

    # Extract data for each channel as a NumPy array
    channel_data = {}
    for channel in channels:
        channel_data[channel] = data[channel].to_numpy()

    # Filter for Delta band (1-4 Hz) with 200 Hz sampling rate
    lowcut = 1
    highcut = 4
    fs = 200

    def butter_bandpass(lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(order, [low, high], btype='bandpass')
        return b, a

    # Filter each channel's data
    filtered_data = {}
    for channel, data in channel_data.items():
        b, a = butter_bandpass(lowcut, highcut, fs)
        filtered_data[channel] = signal.filtfilt(b, a, data)

    # Save the filtered data to a new CSV file
    filtered_data_df = pd.DataFrame(filtered_data)
    filtered_data_df.to_csv(filename.replace('.csv', '_filtered.csv'))

# Usage
filter_data('../data/111g0L.csv')
filter_data('../data/112g0L.csv')
filter_data('../data/113g0R.csv')