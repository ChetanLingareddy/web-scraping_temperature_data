import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv("data.txt")
date = df['date']
temperature = df['temperature']

figure = px.line(x= date,y = temperature, labels={'x': 'date', 'y': 'temperature'})
st.plotly_chart(figure)

