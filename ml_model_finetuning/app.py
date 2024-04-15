# Create a steamlit app with the model that we created
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the model
model = pickle.load(open('models/webapp_model.pkl', 'rb'))

important_features = ['agricultureforestryfishingandhun',
 'heating_degree_days',
 'precipitation_l1',
 'cooling_degree_days',
 'durablegoodsmanufacturing',
 'governmentandgovernmententerpris',
 'utilities',
 'palmer_hydrological_drought_inde',
 'miningquarryingandoilandgasextra',
 'palmer_modified_drought_index_pm']

# Create the UI
st.title('Utah County Wheat Production Prediction')
st.write('This is a simple web app to predict the wheat production in Utah Counties')



# Create the input fields
county = st.selectbox('County', ['Box Elder', 'Cache', 'Weber', 'Utah', 'Salt Lake', 'Davis', 'Tooele', 'Summit', 'Wasatch', 'Morgan'])
year = st.slider('Year', min_value=2002, max_value=2022, value=2020)

agricultureforestryfishingandhun = st.number_input('agricultureforestryfishingandhun', min_value=0, max_value=100000, value=0)
heating_degree_days = st.number_input('heating_degree_days', min_value=0, max_value=100000, value=0)
precipitation_l1 = st.number_input('precipitation_l1', min_value=0, max_value=100000, value=0)
cooling_degree_days = st.number_input('cooling_degree_days', min_value=0, max_value=100000, value=0)
durablegoodsmanufacturing = st.number_input('durablegoodsmanufacturing', min_value=0, max_value=100000, value=0)
governmentandgovernmententerpris = st.number_input('governmentandgovernmententerpris', min_value=0, max_value=100000, value=0)
utilities = st.number_input('utilities', min_value=0, max_value=100000, value=0)
palmer_hydrological_drought_inde = st.number_input('palmer_hydrological_drought_inde', min_value=0, max_value=100000, value=0)
miningquarryingandoilandgasextra = st.number_input('miningquarryingandoilandgasextra', min_value=0, max_value=100000, value=0)
palmer_modified_drought_index_pm = st.number_input('palmer_modified_drought_index_pm', min_value=0, max_value=100000, value=0)

# Create a dictionary to hold the data

data = {
    'county': county,
    'year': year,
    'agricultureforestryfishingandhun': agricultureforestryfishingandhun,
    'heating_degree_days': heating_degree_days,
    'precipitation_l1': precipitation_l1,
    'cooling_degree_days': cooling_degree_days,
    'durablegoodsmanufacturing': durablegoodsmanufacturing,
    'governmentandgovernmententerpris': governmentandgovernmententerpris,
    'utilities': utilities,
    'palmer_hydrological_drought_inde': palmer_hydrological_drought_inde,
    'miningquarryingandoilandgasextra': miningquarryingandoilandgasextra,
    'palmer_modified_drought_index_pm': palmer_modified_drought_index_pm
}

# Create a dataframe
df = pd.DataFrame(data, index=[0])

# Make the prediction
prediction = model.predict(df)

st.write('The predicted wheat production is:', prediction[0])




