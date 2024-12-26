import streamlit as st
import pandas as pd
from io import StringIO

def custom_warning(message):
    st.markdown(f'''
        <p style="
            background-color:#ffffff;
            color:#000000;
            font-size:18px;
            border-radius:5px;
            padding:10px;">
            {message}
        </p>
    ''', unsafe_allow_html=True)


background_image = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://media.istockphoto.com/id/1181555776/vector/pipe-background_2.jpg?s=612x612&w=0&k=20&c=4sBhQ2AaE2gbXgE7C76GyV5MiGAr_tn88gigezSZds4=");
    background-size: 100vw 120vh;  
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html= True)

st.markdown("<h1 style='text-align: center; color: Black; margin-top: 100px; font-family:Arial, Times, serif;'>EOG HYDRATE ALERT</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Save the uploaded file in session state
    st.session_state["uploaded_file"] = uploaded_file
    st.success("File uploaded successfully! Navigate to the Data Analysis Page to visualize the data.")
else:
    custom_warning("Please upload a file to proceed.")


col1, col2, col3, col4,col5,col6 = st.columns(6)

with col6:
     st.page_link("pages\data_page.py", label=":grey-background[Analyze]")

