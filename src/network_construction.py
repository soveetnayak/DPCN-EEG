import pandas as pd
import numpy as np

'''
Construct correlation matrix (CM), use Phase Correlation. So, you see dimension of a CM must be n × n; n= no of channels in time series.
'''
def construct_correlation_matrix(data):
    # Columns start with channel 1
    channels = data.columns[1:]
    
    # Extract data for each channel as a NumPy array
    channel_data = {}
    for channel in channels:
        channel_data[channel] = data[channel].to_numpy()

    # Construct correlation matrix
    correlation_matrix = np.zeros((len(channels), len(channels)))
    for i, (channel1, data1) in enumerate(channel_data.items()):
        for j, (channel2, data2) in enumerate(channel_data.items()):
            correlation_matrix[i, j] = np.corrcoef(data1, data2)[0, 1]

    # Return the correlation matrix
    return correlation_matrix

'''
Binarize the matrix by picking up threshold in such a way so that all the channels are recruited in the network.
'''

def binarize_correlation_matrix(correlation_matrix, threshold):
    binary_matrix = np.zeros(correlation_matrix.shape)
    binary_matrix[correlation_matrix > threshold] = 1
    # Set diagonal to 0
    np.fill_diagonal(binary_matrix, 0)
    # Return the binary matrix
    return binary_matrix

# Usage
threshold = 0.2

for i in range(14):
    data = pd.read_csv(f'../data/111g0L_filtered_fragment_{i}.csv')
    correlation_matrix = construct_correlation_matrix(data)
    binary_matrix = binarize_correlation_matrix(correlation_matrix, threshold)
    # Save as 0 and 1
    np.savetxt(f'../data/binary/111g0L_{i}.csv', binary_matrix, fmt='%d', delimiter=',')

for i in range(14):
    data = pd.read_csv(f'../data/112g0L_filtered_fragment_{i}.csv')
    correlation_matrix = construct_correlation_matrix(data)
    binary_matrix = binarize_correlation_matrix(correlation_matrix, threshold)
    # Save as 0 and 1
    np.savetxt(f'../data/binary/112g0L_{i}.csv', binary_matrix, fmt='%d', delimiter=',')

for i in range(14):
    data = pd.read_csv(f'../data/113g0R_filtered_fragment_{i}.csv')
    correlation_matrix = construct_correlation_matrix(data)
    binary_matrix = binarize_correlation_matrix(correlation_matrix, threshold)
    # Save as 0 and 1
    np.savetxt(f'../data/binary/113g0R_{i}.csv', binary_matrix, fmt='%d', delimiter=',')