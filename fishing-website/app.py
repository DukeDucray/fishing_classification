import streamlit as st
from PIL import Image
import pandas as pd

st.title('Illegal Fishing')

st.markdown('''
Below is a map of sample fishing events around the world 🗺''')

image = Image.open('../data/output.png')

st.image(image, caption='Fishing events around the World')

st.file_uploader("Please upload the csv of the boat your would like to track")

st.markdown('''
Our goal is to predict based on the boat's trajectory events went it was fishing or not as well as predict the fishing gear used by the boat''')
boat_longitude = st.number_input('Current Boat\'s Longitude', value=-73.950655, step=1e-7, format="%.6f")
boat_latitude = st.number_input('Current Boat\'s Latitude', value=40.783282, step=1e-7, format="%.6f")

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''
