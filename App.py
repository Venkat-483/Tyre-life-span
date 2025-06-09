import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the trained model
model = joblib.load("best_tyre_model.pkl")

st.title("Tyre Safety Prediction")
st.write("Enter the tyre and vehicle parameters to check if the tyre is safe.")

# User input fields
tread_depth = st.number_input("Tread Depth (mm)", min_value=0.0, step=0.1)
tire_pressure = st.number_input("Tire Pressure (psi)", min_value=0.0, step=0.1)
temperature = st.number_input("Temperature (°C)", min_value=-50.0, step=0.1)
vibration_mean = st.number_input("Vibration Mean (g)", min_value=0.0, step=0.01)
vibration_std = st.number_input("Vibration Std (g)", min_value=0.0, step=0.01)
wheel_rpm = st.number_input("Wheel Speed (rpm)", min_value=0)
speed_kmh = st.number_input("Speed (km/h)", min_value=0.0, step=0.1)
odometer = st.number_input("Odometer (km)", min_value=0)
rider_weight = st.number_input("Rider Weight (kg)", min_value=0.0, step=0.1)
punctures = st.number_input("Number of Punctures", min_value=0)

road_type = st.radio("Road Type", ["City", "Highway", "OffRoad"])

# One-hot encoding for RoadType
road_city, road_highway, road_offroad = 0, 0, 0
if road_type == "City":
    road_city = 1
elif road_type == "Highway":
    road_highway = 1
else:
    road_offroad = 1

if st.button("Predict Tyre Safety"):
    # Create DataFrame
    input_data = pd.DataFrame({
        "TreadDepth_mm": [tread_depth],
        "TirePressure_psi": [tire_pressure],
        "Temperature_C": [temperature],
        "VibrationMean_g": [vibration_mean],
        "VibrationStd_g": [vibration_std],
        "WheelSpeed_rpm": [wheel_rpm],
        "Speed_km_h": [speed_kmh],
        "Odometer_km": [odometer],
        "RiderWeight_kg": [rider_weight],
        "NumberOfPunctures": [punctures],
        "RoadType_City": [road_city],
        "RoadType_Highway": [road_highway],
        "RoadType_OffRoad": [road_offroad]
    })

    # Prediction
    predicted_life = model.predict(input_data)[0]

    st.write(f"### Predicted Remaining Life: {predicted_life:.2f} km")

    if predicted_life >= 2000:
        st.success("✅ The tyre is SAFE.")
    else:
        st.error("❌ The tyre is NOT SAFE.")
