# Create a steamlit app with the model that we created
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the model
model = pickle.load(open('model.pkl', 'rb'))

# Create the UI
st.title('House Price Prediction')


