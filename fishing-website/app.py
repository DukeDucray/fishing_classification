import streamlit as st
import pandas as pd
import datetime
import requests

from PIL import Image

# Title
st.title('Illegal Fishing')

# Map
st.markdown('''
Below is a map of sample fishing events around the world 🗺''')
image = Image.open('../data/output.png')
st.image(image, caption='Fishing events around the World')

# Information below map
st.markdown('''
Our goal is to predict based on the boat's trajectory events went it was fishing
or not as well as predict the fishing gear used by the vessel''')

# Upload csv information
st.set_option('deprecation.showfileUploaderEncoding', False)
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)

# Select specific location
date_time_position = st.date_input("Set date", value=datetime.datetime(2019,7,6))
boat_longitude = st.number_input('Current Boat\'s Longitude', value=-73.950655, step=1e-7, format="%.6f")
boat_latitude = st.number_input('Current Boat\'s Latitude', value=40.783282, step=1e-7, format="%.6f")

# Dictionary containing the parameters for our API...
params = dict(
    pickup_datetime=date_time_position,
    boat_longitude=boat_longitude,
    boat_latitude=boat_latitude,
    dropoff_longitude=dropoff_longitude,
    dropoff_latitude= dropoff_latitude,
    passenger_count= passenger_count,
    )

# URL to call
url = ''

if st.button("Is this boat fishing"):
    res = requests.get(url, params=params).json()
    st.subheader(f"The estimated fare is ${round(res['fare'],2)}")

if st.button("What type of gear is this boat using"):
    res = requests.get(url, params=params).json()
    st.subheader(f"The estimated fare is ${round(res['fare'],2)}")
