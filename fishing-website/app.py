import streamlit as st
import pandas as pd
import datetime
import requests
import folium

from streamlit_folium import st_folium, folium_static
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

    if st.button("Check this boat"):
        place_lat=data["lat"].tolist()
        place_lng=data["lon"].tolist()
        num = round(len(place_lat)/2)

        base_map = folium.Map(location=[place_lat[num], place_lng[num]], control_scale=True)

        df_fishing = data[data['is_fishing']==1]
        fishing = list(zip(df_fishing.lat, df_fishing.lon))

        df_not_fishing = data[data['is_fishing']==0]
        not_fishing = list(zip(df_not_fishing.lat, df_not_fishing.lon))

        for fish in fishing:
            icon=folium.Icon(color='white', icon_color="yellow")
            folium.Marker(fish, icon=icon).add_to(base_map)

        for notfish in not_fishing:
            icon=folium.Icon(color='white', icon_color="red")
            folium.Marker(notfish, icon=icon).add_to(base_map)

        points = []
        for i in range(len(place_lat)):
            points.append([place_lat[i], place_lng[i]])

        folium.PolyLine(locations=points, color='green').add_to(base_map)

        sw = data[['lat', 'lon']].min().values.tolist()
        ne = data[['lat', 'lon']].max().values.tolist()
        base_map.fit_bounds([sw, ne])

        folium_static(base_map)


    if st.button("What type of gear is this boat using?"):
        res = requests.get(url, params=params).json()
        st.subheader(f"The boat is using {res['result']}")
