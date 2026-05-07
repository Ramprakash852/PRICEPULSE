import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/products"

response = requests.get(API_URL)

data = response.json()

df = pd.DataFrame(data)

st.title("PricePulse Dashboard")

st.subheader("Competitor Product Monitoring")

st.dataframe(df)

st.subheader("Top Rated Products")

top_rated = df[df["rating"] >= 4]

st.dataframe(top_rated)

st.subheader("Price Statistics")

st.write(df["price"].describe())