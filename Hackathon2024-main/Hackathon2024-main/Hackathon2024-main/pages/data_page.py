import streamlit as st
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

st.markdown("<h2>Data Analysis Page</h2>", unsafe_allow_html=True)



if "uploaded_file" in st.session_state and st.session_state["uploaded_file"] is not None:
    
    uploaded_file = st.session_state["uploaded_file"]
    data = pd.read_csv(uploaded_file)

    # Step 1: Data Cleaning
    # Convert 'Time' column to datetime format
    data['Time'] = pd.to_datetime(data['Time'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    # Drop rows with missing critical data
    data_cleaned = data.dropna(subset=['Inj Gas Meter Volume Instantaneous', 'Inj Gas Valve Percent Open'])
    # Interpolate missing Setpoint values
    data_cleaned['Inj Gas Meter Volume Setpoint'] = data_cleaned['Inj Gas Meter Volume Setpoint'].interpolate()

    # Step 2: Visualization of All Columns
    st.write("Trend Analysis:")
    # Center the chart in the middle of the app
    with st.container():
        fig, ax = plt.subplots(figsize=(12, 6))  # Adjusted size for compactness
        ax.plot(data_cleaned['Time'], data_cleaned['Inj Gas Meter Volume Instantaneous'], label='Instantaneous Volume', color='green')
        ax.plot(data_cleaned['Time'], data_cleaned['Inj Gas Meter Volume Setpoint'], label='Setpoint Volume', color='red', linestyle='dashed')
        ax.plot(data_cleaned['Time'], data_cleaned['Inj Gas Valve Percent Open'], label='Valve Percent Open (%)', color='blue')

        ax.set_title("Gas Injection Trends")
        ax.set_xlabel("Time")
        ax.set_ylabel("Values")
        ax.legend()
        ax.grid()

        st.pyplot(fig)

    # Step 3: Load the data
    
    st.write("Uploaded Data:")
    
    st.dataframe(data, width=800, height=500)

    # Read the uploaded file
    
    st.success("Warning(s) Log")
    
    # Process the file and detect hydrate warnings
    warnings = []
    pipeOpen = True
    ignore = False
    previousVolume = data.iloc[0]['Inj Gas Meter Volume Instantaneous']
    previousValve = data.iloc[0]['Inj Gas Valve Percent Open']

    for index in range(len(data)):
        valve = data.iloc[index]['Inj Gas Valve Percent Open'] if not pd.isna(data.iloc[index]['Inj Gas Valve Percent Open']) else previousValve
        volume = data.iloc[index]['Inj Gas Meter Volume Instantaneous'] if not pd.isna(data.iloc[index]['Inj Gas Meter Volume Instantaneous']) else previousVolume

        if previousVolume == 0 and volume != 0:
            pipeOpen = True
        if previousValve == 100 and valve != 100:
            ignore = False

        jump = valve - previousValve
        if valve == 100 and jump < 50:
            if ignore:
                ignore = False
                continue
            else:
                if volume == 0 and pipeOpen:
                    warning_msg = f"Hydrate formation detected on {data.iloc[index]['Time']}"
                    warnings.append(warning_msg)
                    st.toast(warning_msg, icon="⚠️")  # Display as a notification
                    st.error(warning_msg, icon="🚨")
                    pipeOpen = False

        if jump > 50:
            ignore = True

        previousVolume = volume
        previousValve = valve

    
else:
    st.warning("Please upload a file to proceed.")

