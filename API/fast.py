import pandas as pd
import os
from fastapi import FastAPI, UploadFile, File
import io

from joblib import load

from code_for_API.preproc import preproc


# Load the trained model
current_directory = os.getcwd()
target_directory = os.path.join(current_directory, 'API/data/model')
model_path = os.path.join(target_directory, 'rf_model.joblib')
print(model_path)
loaded_model = load(model_path)


app = FastAPI()
app.state.model = loaded_model

@app.post("/predict")
async def predict(csv_file_df):
    """
    Predict if the boat is fishing or not.
    Return DataFrame with 'is_fishing' column.
    """
    # Process uploaded CSV file and return DataFrame
    df = preproc(csv_file_df)  # Replace with your preproc function

    # Assuming you preprocess the DataFrame and drop certain columns
    df = df.drop(columns=['source', 'date', 'hour'])

    #Run model
    y_pred = app.state.model.predict(df)

    # Convert y_pred to a Python list
    y_pred_list = y_pred.tolist()

    # Update the 'is_fishing' column with the predictions
    df['is_fishing'] = y_pred_list

    # Convert DataFrame to a JSON-serializable format (e.g., a list of dictionaries)
    response_dict = df.to_dict(orient='list')

    return response_dict


@app.get("/sample")
def sample(sample_request: str,):      # 1
    """
    Use one of our sample track data to visualize how our model work.
    our sample range between 1 and 20
    """
    sample_names = ['trawlers', 'drifting_longlines', 'fixed_gear', 'pole_and_line', 'purse_seines', 'trollers', 'unknown']

    if sample_request not in sample_names:
        return {"error" : f"No sample with this name please choose between these sameple: {sample_names}" }


    data_folder = os.path.join(os.path.dirname(__file__), "data", "sample_data")
    file_path = os.path.join(data_folder, f"sample_{sample_request}.csv")

    df = pd.read_csv(file_path)

    #Run model
    y_pred = app.state.model.predict(df)

    # Convert y_pred to a Python list
    y_pred_list = y_pred.tolist()

    # Update the 'is_fishing' column with the predictions
    df['is_fishing'] = y_pred_list

    # Convert DataFrame to a JSON-serializable format (e.g., a list of dictionaries)
    response_dict = df.to_dict(orient='list')

    return response_dict




@app.get("/")
def root():
    return {
        'greeting': 'Hello'
    }



# Run the Uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
