import pandas as pd

'''
Truncate the original iEEG time series by taking all the seizure time points along with 5000 time points from before as well as after seizure.
file_id     episode     start       dt  SzOnLoc         tend	tend_sec	tsz	    tsz_sec	dt_s
111	        15:42:30    15:40:46	104	L mesial temp	43101	215.505	    34974	174.87	40.635
112	        17:04:35    17:02:51	104	L mesial temp	38828	194.14	    26999	134.995	59.145
113	        19:42:49    19:41:06	103	R mesial temp	35820	179.1	    25562	127.81	51.29
'''

def truncate_data(data, dt, tstart, tend):
    
    channels = data.columns[1:]

    # Extract data for each channel as a NumPy array
    channel_data = {}
    for channel in channels:
        channel_data[channel] = data[channel].to_numpy()

    # Truncate data start-5000:end+5000
    truncated_data = {}
    for channel, data in channel_data.items():
        truncated_data[channel] = data[tstart-5000:tend+5000]

    # Save the truncated data to a new CSV file
    truncated_data_df = pd.DataFrame(truncated_data)
    return truncated_data_df

'''
Fragmentize the truncated time series into 14 parts.
Scheme: b/f seizure + seizure + a/f seizure = 2+10+2
Length of the fragments, separately in the three regions, must be identical.
'''

def fragmentize_data(data, dt, tstart, tend):

    channels = data.columns[1:]

    # Extract data for each channel as a NumPy array
    channel_data = {}
    for channel in channels:
        channel_data[channel] = data[channel].to_numpy()

    # Fragmentize data into 14 parts
    fragmentized_data = {}
    for channel, data in channel_data.items():
        fragmentized_data[channel] = []
        fragment_size = int(len(data)/14)
        for i in range(0, len(data), fragment_size):
            fragmentized_data[channel].append(data[i:i+fragment_size])

    # Return the fragmentized data
    return fragmentized_data

'''
Remove reference channels and any channels that start with G, F, I. Column names must be only the channel names without any other characters in the string.
Reference channels after cleaning: TLR03, TLR04
'''

def channel_cleaning(data):
    # Columns start with channel 1
    channels = data.columns[1:]
    cleaned_channels = []
    
    # b'SEEG TBAL1' -> TBAL1
    for channel in channels:
        cleaned_channels.append(channel.split()[-1].decode('utf-8'))

    # Remove reference channels and any channels that start with G, F, I
    cleaned_channels = [channel for channel in cleaned_channels if not channel.startswith('G') and not channel.startswith('F') and not channel.startswith('I') and channel not in ['TLR03', 'TLR04']]

    # Extract data for each channel as a NumPy array
    channel_data = {}
    for channel in cleaned_channels:
        channel_data[channel] = data[channel].to_numpy()

    # Save the cleaned data to a new CSV file
    cleaned_data_df = pd.DataFrame(channel_data)
    return cleaned_data_df
