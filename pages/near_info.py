# https://groq.com/ 사용

import streamlit as st
import pandas as pd
import numpy as np

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

@st.cache_data
def load_data():
    df = pd.read_csv("data_6_store_lat_lon.csv")
    return df

df = load_data()

def find_closest_building(address, df):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)
    
    if not location:
        return "주소를 찾을 수 없습니다.", None, None

    full_address = location.address
    print(f'위도 : {location.latitude}, 경도: {location.longitude}')
    input_coords = (location.latitude, location.longitude)

    df['distance'] = df.apply(
        lambda row: geodesic(input_coords, (row['lat'], row['lon'])).meters,
        axis=1
    )

    closest = df.loc[df['distance'].idxmin()]
    return full_address, closest['name'], closest['distance']

address_text = st.text_input('주소를 입력하세요: ')
accept = st.button('검색')

full_address, building, distance = find_closest_building(address_text, df)

if accept :
    # st.code(code_str)
    

    if building:
        st.write(eval("df[df['name'] == '지에스25SH상암']"))
        print(f"[입력 주소 보정] {full_address}")
        print(f"[가장 가까운 빌딩] {building}")
        print(f"[거리] {distance:.2f} 미터")
    else:
        st.write("주소를 찾을 수 없습니다. 정확한 주소를 입력해주세요")
        print(full_address)