import streamlit as st
import pandas as pd
from AntiML import EDA
from Prediction import predict

# Load Data
@st.cache_data
def load_datasets():
# Load data from local files
    li_small = pd.read_csv("LI-Small_Trans.csv", header=0, parse_dates=[0])
    hi_small = pd.read_csv("HI-Small_Trans.csv", header=0, parse_dates=[0])
    return li_small, hi_small

# Load the datasets
li_small, hi_small = load_datasets()
    
# Define a function to switch pages
def switch_page(page_name: str):
    st.session_state["page"] = page_name
    st.experimental_rerun()

# Initialize session state for page
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Sidebar with navigation buttons
st.sidebar.header("Navigation")
if st.sidebar.button("Home", key="home_button"):
    switch_page("home")
if st.sidebar.button("Prediction", key="predict_button"):
    switch_page("predict")

# Display content based on the current page
if st.session_state["page"] == "home":
    EDA(li_small, hi_small)
elif st.session_state["page"] == "predict":
    predict(li_small)
else:
    st.error("Page not found: " + st.session_state["page"])