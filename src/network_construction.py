import pandas as pd
import numpy as np

'''
Step 1- To construct correlation matrix (CM), use Phase Correlation. So, you see dimension of a CM must be n × n; n= no of channels in time series.
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
Step 2- Binarize the matrix by picking up threshold in such a way so that all the channels are recruited in the network.
'''

def binarize_correlation_matrix(correlation_matrix, threshold):
    binary_matrix = np.zeros(correlation_matrix.shape)
    binary_matrix[correlation_matrix > threshold] = 1

    # Return the binary matrix
    return binary_matrix

