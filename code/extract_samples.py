import pandas as pd
import os

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


from code_for_API.preproc import preproc
## process raw data for pipeline

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
folder_path = "API/data/sample_data"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print("Folder created successfully.")
else:
    print("Folder already exists.")

# # Extract all sample to .csv
path='data/raw_data'
file_names = ['trawlers', 'drifting_longlines', 'fixed_gear', 'pole_and_line', 'purse_seines', 'trollers', 'unknown']

for file_name in file_names:
    df = get_data(path, file_name)

    data = extract_sample(df)

    df = preproc(data)

    send_csv(df, file_name)
