import pandas as pd
import numpy as np

# # get_data

def get_data(path, file_names):
    return pd.read_csv(f'../{path}/{file_name}.csv')

# # extract_sample
def extract_sample(X):
    grouped = X.groupby('mmsi')

    # Get the first group's key (value in the 'mmsi' column)
    first_group_key = list(grouped.groups.keys())[0]

    # Get the first group as a DataFrame
    first_group_df = pd.DataFrame(grouped.get_group(first_group_key))

    return first_group_df


# # Send CSV sample
def send_csv(df, file_name):
    output_folder = '../API/data/sample_data'
    output_file = f'sample_{file_name}.csv'

    # Construct the full path
    output_path = f'{output_folder}/{output_file}'

    # Save the DataFrame to the specified path
    df.to_csv(output_path, index=False)

    print(f"{output_file} saved at: {output_folder}")

# # Extract all sample to .csv
path='data/raw_data'
file_names = ['trawlers', 'drifting_longlines', 'fixed_gear', 'pole_and_line', 'purse_seines', 'trollers', 'unknown']

for file_name in file_names:
    df = get_data(path, file_name)

    data = extract_sample(df)

    send_csv(data, file_name)
