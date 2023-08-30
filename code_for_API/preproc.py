
import pandas as pd

def preproc(df_fishing):
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


def model_train_preproc(df):

    # ## Remove unknown (-1 in is_fishing column)
    df_fishing = df.loc[df['is_fishing'] > -1]

    # round the decimals so that number becomes 0 or 1
    df_fishing.loc[:, ('is_fishing')] = round(df_fishing.loc[:, ('is_fishing')])

    # ## remove type, as it is target of second model
    df_fishing.drop(columns = ["type"], inplace = True)

    # ## Date time (hour -> Angular distance)
    df_fishing['timestamp'] = pd.to_datetime(df_fishing['timestamp'], unit='s')
    df_fishing.rename(columns={"timestamp": "date"}, inplace=True)
    df_fishing['hour'] = df_fishing['date'].dt.hour
    df_fishing['month'] = df_fishing['date'].dt.month
    df_fishing['day_of_week'] = df_fishing['date'].dt.day_of_week

    #
    df_fishing['hour_sin'] = np.sin(df_fishing['hour'] * (2 * np.pi / 24))
    df_fishing['hour_cos'] = np.cos(df_fishing['hour'] * (2 * np.pi / 24))

    # ## remove boat history track that are too small ( <15 )
    # Calculate the value counts of 'mmsi'
    mmsi_counts = df_fishing['mmsi'].value_counts()

    # Create a boolean mask for filtering mmsi values with counts less than or equal to 15
    mask = mmsi_counts > 15

    # Get the mmsi values that meet the condition
    selected_mmsi = mmsi_counts[mask].index

    # Use the isin() method to filter the DataFrame based on selected_mmsi
    filtered_fishing_df = df_fishing[df_fishing['mmsi'].isin(selected_mmsi)]

    # Dropping rows with NAN values
    df_fishing_clean = filtered_fishing_df.dropna()

    return df_fishing_clean
