import pandas as pd
import numpy as np

# # get_data
def get_data(path, file_name):
    return pd.read_csv(f'{path}/{file_name}.csv')

# # extract_sample
def extract_sample(X):
    grouped = X.groupby('mmsi')

    # Get the first group's key (value in the 'mmsi' column)
    first_group_key = list(grouped.groups.keys())[0]

    # Get the first group as a DataFrame
    first_group_df = pd.DataFrame(grouped.get_group(first_group_key))

    first_group_df_cleaned = first_group_df.drop(columns=['source', 'is_fishing'])

    return first_group_df_cleaned

## process raw data for pipeline
def sample_preproc(df_fishing):
    # ## Date time (hour -> Angular distance)
    df_fishing['timestamp'] = pd.to_datetime(df_fishing['timestamp'], unit='s')
    df_fishing.rename(columns={"timestamp": "date"}, inplace=True)
    df_fishing['hour'] = df_fishing['date'].dt.hour
    df_fishing['month'] = df_fishing['date'].dt.month
    df_fishing['day_of_week'] = df_fishing['date'].dt.day_of_week

    #
    df_fishing['hour_sin'] = np.sin(df_fishing['hour'] * (2 * np.pi / 24))
    df_fishing['hour_cos'] = np.cos(df_fishing['hour'] * (2 * np.pi / 24))

    # Dropping rows with NAN values
    df_fishing_clean = df_fishing.dropna()

    X = df_fishing_clean.drop(columns=['date','hour'])

    return X



# # Send CSV sample
def send_csv(df, file_name):
    output_folder = 'API/data/sample_data'
    output_file = f'sample_{file_name}.csv'

    # Construct the full path
    output_path = f'{output_folder}/{output_file}'

    # Save the DataFrame to the specified path
    df.to_csv(output_path, index=False)

    print(f"{output_file} saved at: {output_folder}")


# MAIN
# # Extract all sample to .csv
path='data/raw_data'
file_names = ['trawlers', 'drifting_longlines', 'fixed_gear', 'pole_and_line', 'purse_seines', 'trollers', 'unknown']

for file_name in file_names:
    df = get_data(path, file_name)

    data = extract_sample(df)

    df = sample_preproc(data)

    send_csv(df, file_name)
