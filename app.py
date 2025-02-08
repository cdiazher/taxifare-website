import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.markdown("# Calculate your Taxi fare")

col1, col2, col3, col4, col5 = st.columns([1,2,2,1,1])
with col1:
    date = st.date_input("Pick-up Date", value="2025-02-08")
    default_time = datetime.strptime("12:00:00", "%H:%M:%S").time()
    time = st.time_input("Pick-up Time", value=default_time)
    date_time = datetime.combine(date, time)
with col2:
    pickup_longitude = st.number_input("Pick-up Longitude", value=-73.935242)
    pickup_latitude = st.number_input("Pick-up Latitude", value=40.730610)
with col3:
    dropoff_longitude = st.number_input("Drop-off Longitude", value=-73.980713)
    dropoff_latitude = st.number_input("Drop-off Latitude", value=40.741060)
with col4:
    passenger_count = st.number_input("Passenger Count", min_value=1, max_value=6, value=1)


url = 'https://taxifare.lewagon.ai/predict'

parameters = {
    'pickup_datetime': date_time.strftime("%Y-%m-%d %H:%M:%S"),
    'pickup_longitude': pickup_longitude,
    'pickup_latitude': pickup_latitude,
    'dropoff_longitude': dropoff_longitude,
    'dropoff_latitude': dropoff_latitude,
    'passenger_count': passenger_count
}

with col5:
    if st.button('Get Fare'):
        response = requests.get(url, params=parameters)

        if response.status_code == 200:
            prediction = response.json()['fare']
            st.success(f"${prediction:.2f}")
        else:
            st.error("Try again.")

map = folium.Map(location=[(pickup_latitude + dropoff_latitude) / 2,
                           (pickup_longitude + dropoff_longitude) / 2],
                 zoom_start=20)
folium.Marker(
    location=[pickup_latitude, pickup_longitude],
    popup="📍Pickup",
    icon=folium.Icon(color="blue", icon="info-sign"),
).add_to(map)

folium.Marker(
    location=[dropoff_latitude, dropoff_longitude],
    popup="📍Dropoff",
    icon=folium.Icon(color="blue", icon="info-sign"),
).add_to(map)

folium.PolyLine(
    locations=[[pickup_latitude, pickup_longitude], [dropoff_latitude, dropoff_longitude]],
    color="black",
    weight=5,
    opacity=0.7,
).add_to(map)

st_folium(map)
