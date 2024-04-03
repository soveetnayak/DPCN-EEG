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

def fragmentize_data(data, filename):
    channels = data.columns[1:]
    len = data.shape[0]
    fragment_length = len//14

    channel_data = {}
    for channel in channels:
        channel_data[channel] = data[channel]

    # Fragmentize data
    for i in range(14):
        fragment = {}
        for channel, data in channel_data.items():
            fragment[channel] = data[i*fragment_length:(i+1)*fragment_length]
        fragment_df = pd.DataFrame(fragment)
        fragment_df.to_csv(filename.replace('.csv', f'_fragment_{i}.csv'))


'''
Remove reference channels and any channels that start with G, F, I. Column names must be only the channel names without any other characters in the string.
Reference channels after cleaning: "b'SEEG TLR03'","b'SEEG TLR04'"
'''

def channel_cleaning(data):
    data = data.drop(columns=["b\'SEEG TLR03\'", "b\'SEEG TLR04\'"])

    channels = data.columns[1:]
    cleaned_channels = []

    # "b'SEEG TBAL1'" -> "TBAL1"
    for channel in channels:
        cleaned_channels.append(channel.split()[-1].replace("'", ""))
    # Rename the columns
    data.columns = [''] + cleaned_channels
    # Remove any channels that start with G, F, I
    data = data.drop(columns=[channel for channel in cleaned_channels if channel.startswith(('G', 'F', 'I'))])

    return data

#Usage
data = pd.read_csv('../data/111g0L_filtered.csv')
truncated_data = truncate_data(data, 104, 34974, 43101)
cleaned_data = channel_cleaning(truncated_data)
fragmentize_data(cleaned_data, '../data/111g0L_filtered.csv')

data = pd.read_csv('../data/112g0L_filtered.csv')
truncated_data = truncate_data(data, 104, 26999, 38828)
cleaned_data = channel_cleaning(truncated_data)
fragmentize_data(cleaned_data, '../data/112g0L_filtered.csv')

data = pd.read_csv('../data/113g0R_filtered.csv')
truncated_data = truncate_data(data, 103, 25562, 35820)
cleaned_data = channel_cleaning(truncated_data)
fragmentize_data(cleaned_data, '../data/113g0R_filtered.csv')