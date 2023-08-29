import streamlit as st
import pandas as pd
import datetime
import requests
import folium

from streamlit_folium import st_folium
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
Our goal is to predict based on the boat's trajectory, instances when the boat was fishing
as well as predict the fishing gear used by the vessel''')

# Upload csv information
st.set_option('deprecation.showfileUploaderEncoding', False)
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)

# URL to call
url = ''

if st.button("Is this boat fishing?"):
    res = requests.get(url, params=params).json()
    st.subheader(f"The boat is fishing${res['fare']}")

if st.button("What type of gear is this boat using?"):
    res = requests.get(url, params=params).json()
    st.subheader(f"The boat is using ${res['fare']}")


map = folium.Map(location=[37.4601908, 126.4406957],
               zoom_start=15)

place_lat = [37.4601928, 37.4593108, 37.4641108, 37.4611508]
place_lng = [126.4406957, 126.4432957, 126.4476917, 126.4423957]

points = []
for i in range(len(place_lat)):
    points.append([place_lat[i], place_lng[i]])

for index,lat in enumerate(place_lat):
    folium.Marker([lat,
                   place_lng[index]],
                  popup=('patient{} \n 74contacts'.format(index)),
                 icon = folium.Icon(color='green',icon='plus')).add_to(map)
folium.PolyLine(points, color='red').add_to(map)

st_folium(map)
