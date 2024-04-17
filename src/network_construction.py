import pandas as pd
import numpy as np
import networkx as nx
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

def binarize_correlation_matrix(correlation_matrix):
    # Start as threshold = 1 with step -0.1
    # As soon as all the channels are recruited, stop and return the binary matrix
    # GCC of the binary matrix is the network
    threshold = 1
    while True:
        binary_matrix = np.where(correlation_matrix > threshold, 1, 0)
        # diagonal elems 0
        np.fill_diagonal(binary_matrix, 0)
        
        # Check if all the channels are recruited. Recruited means the graph is connected.        
        if nx.is_connected(nx.convert_matrix.from_numpy_array(binary_matrix)):
            print(f'Threshold: {threshold}')
            break

        if threshold < 0:
            break
        threshold -= 0.1

    return binary_matrix


for i in range(14):
    print(f'Processing 111g0L_{i}')
    data = pd.read_csv(f'../data/111g0L_filtered_fragment_{i}.csv')
    correlation_matrix = construct_correlation_matrix(data)
    binary_matrix = binarize_correlation_matrix(correlation_matrix)
    # Save as 0 and 1
    np.savetxt(f'../data/binary/111g0L_{i}.csv', binary_matrix, fmt='%d', delimiter=',')

for i in range(14):
    print(f'Processing 112g0L_{i}')
    data = pd.read_csv(f'../data/112g0L_filtered_fragment_{i}.csv')
    correlation_matrix = construct_correlation_matrix(data)
    binary_matrix = binarize_correlation_matrix(correlation_matrix)
    # Save as 0 and 1
    np.savetxt(f'../data/binary/112g0L_{i}.csv', binary_matrix, fmt='%d', delimiter=',')