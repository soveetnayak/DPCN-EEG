import h5py
import numpy as np
import pandas as pd


def convert_hdf5_to_csv(hdf5_file_path, output_csv_path):
    # Read the HDF5 file
    with h5py.File(hdf5_file_path, "r") as file:
        eeg = file.get("EEG")
        # Get the keys of all datasets in the HDF5 file
        column_names_dataset = np.array(eeg.get("block0_items"))
        matrix_dataset = np.array(eeg.get("block0_values"))

    # Convert the matrix to a DataFrame with column names
    df = pd.DataFrame(matrix_dataset, columns=column_names_dataset)

    # Save the data to CSV
    df.to_csv(output_csv_path)


# Usage for multiple files
input_hdf5_files = [
    r"../data/111g0L.h5",
    r"../data/112g0L.h5",
    r"../data/113g0R.h5",
]

output_csv_paths = [
    r"../data/111g0L.csv",
    r"../data/112g0L.csv",
    r"../data/113g0R.csv",
]

for input_hdf5_file, output_csv_path in zip(input_hdf5_files, output_csv_paths):
    convert_hdf5_to_csv(input_hdf5_file, output_csv_path)
