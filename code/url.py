import os


sample_name = 'trawlers'  # Replace this with the sample name you want to use

# Define the API endpoint URL
base_url = "http://localhost:8000"  # Change this if your server is hosted elsewhere
endpoint = "/sample"

# Create the complete URL
url = f"{base_url}{endpoint}?sample_request={sample_name}"

print (url)

sample_request='trawlers'

data_folder = os.path.join(os.path.dirname(__file__), "data", "sample_data")
file_path = os.path.join(data_folder, f"sample_{sample_request}.csv")

print(file_path)
