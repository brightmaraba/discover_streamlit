import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import os

this_file_path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(this_file_path)
DATA = os.path.join(BASE_DIR, 'data')
STATIC_IMAGES = os.path.join(BASE_DIR, 'static_images')

st.set_page_config(page_title='Food Prediction', page_icon='🍔', layout='wide')
st.title('Food Demand Forecasting - B. Koech')
st.sidebar.title('Food Demand Prediction')
st.sidebar.image(os.path.join(STATIC_IMAGES, 'flourish.png'), use_column_width=True)

@st.cache
def load_data(nrows):
    data = pd.read_csv(os.path.join(DATA, 'train.csv'), nrows=nrows)
    return data

@st.cache
def load_center_data(nrows):
    data = pd.read_csv(os.path.join(DATA, 'fulfilment_center_info.csv'), nrows=nrows)
    return data

@st.cache
def load_meal_data(nrows):
    data = pd.read_csv(os.path.join(DATA, 'meal_info.csv'), nrows=nrows)
    return data

data_load_state = st.text('Loading data...')
weekly_data = load_data(1000)
center_info_data = load_center_data(10000)
meal_data = load_meal_data(10000)

# Bar chart of Weekly Demand Data
st.subheader('Weekly Demand')
col1, col2 = st.columns(2)

with col1:
    """
    #### Raw Data
    """
    st.write(weekly_data)
with col2:
    """
    #### Number of Meal Orders Per Client
    """
    source = alt.Chart(weekly_data.reset_index()).mark_bar().encode(
        x='index',
        y='num_orders'
    )
    st.altair_chart(source, use_container_width=True)

# Histograms
st.subheader('Histograms of Weekly Demand')
df = pd.DataFrame(weekly_data[:200], columns=['num_orders', 'checkout_price', 'base_price'])
col1, col2, col3 = st.columns(3)
with col1:
    """
    #### Number of Orders
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(df['num_orders'], bins=20)
    st.pyplot(fig)

with col2:
    """
    #### Checkout Price
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(df['checkout_price'], bins=20)
    st.pyplot(fig)

with col3:
    """
    #### Base Price
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(df['base_price'], bins=20)
    st.pyplot(fig)

# Line Chart
st.subheader('Weekly Demand - Base Price, Checkout Price, Number of Orders')
st.line_chart(df)

# Area Chart
st.subheader('Weekly Demand - Base Price, Number of Orders')
chart_data = pd.DataFrame(weekly_data[:40], columns=['num_orders', 'base_price'])
st.area_chart(chart_data)

st.subheader('Fulfillment Center Information')
if st.checkbox('Show Center Information Data'):
    st.subheader('Fulfillment Center Information Data')
    st.write(center_info_data)

st.bar_chart(center_info_data['region_code'])
chart = alt.Chart(center_info_data).mark_bar().encode(
        alt.X('center_type'),
        y='count()'
    )
st.altair_chart(chart, use_container_width=True)

# Distribution
hist_data = [center_info_data['center_id'], center_info_data['region_code']]
group_labels = ['center_id', 'region_code']
fig = ff.create_distplot(hist_data, group_labels, bin_size=[10, 15])
st.plotly_chart(fig, use_container_width=True)
