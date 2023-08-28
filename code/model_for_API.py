#
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, classification_report

from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

from code_for_API.preproc import preproc

import warnings
warnings.filterwarnings('ignore')


# # Get raw data
def get_data(path, file_names):
    tables=[]
    for file_name in file_names:
        table = pd.read_csv(f'../{path}/{file_name}.csv')
        table['type']=f'{file_name}'
        tables.append(table)
    return pd.concat(tables)

path='data/raw_data'
file_names = ['trawlers', 'drifting_longlines', 'fixed_gear', 'pole_and_line', 'purse_seines', 'trollers', 'unknown']
df = get_data(path, file_names)

df_fishing_clean = preproc(df)

# # Split Data
# Defining X - the features and Y - the target
X = df_fishing_clean.drop(columns=['source','date','hour','is_fishing'])
y = df_fishing_clean['is_fishing']

#
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=88)

# # Make Pipeline
# ## OHE month and day of week and scaling for the rest
# Define the columns that need different preprocessing
numeric_cols = ['mmsi', 'distance_from_shore', 'distance_from_port', 'speed', 'course']
minmax_cols = ['lat', 'lon']
ohe_cols = ['month', 'day_of_week']

# Create transformers for each type of preprocessing
numeric_transformer = StandardScaler()
minmax_transformer = MinMaxScaler()
ohe_transformer = OneHotEncoder(drop='first', sparse=False)

# Create a ColumnTransformer to apply different transformers to different columns
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_cols),
        ('minmax', minmax_transformer, minmax_cols),
        ('ohe', ohe_transformer, ohe_cols),
        ('passthrough', 'passthrough', ['hour_sin', 'hour_cos'])  # Bypass these features
    ])

# Create the Random Forest Classifier model
rf_model = RandomForestClassifier()

# Create the pipeline using make_pipeline
pipeline = make_pipeline(preprocessor, rf_model)

# # Train Model
# Train Pipeline
pipeline.fit(X_train,y_train)
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f} Precision:{precision:.2f}")

# # Export Model
from joblib import dump
import os

# Get the current directory
current_directory = os.getcwd()

# Navigate to the desired directory
target_directory = os.path.join(current_directory, '..', 'API/data/model')
# Create the target directory if it doesn't exist
os.makedirs(target_directory, exist_ok=True)

# Define the path for saving the model
model_path = os.path.join(target_directory, 'rf_model.joblib')

# Save the trained model to the specified path
dump(pipeline, model_path)

print(f"Model saved at: {model_path}")
