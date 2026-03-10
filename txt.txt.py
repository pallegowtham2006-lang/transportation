import streamlit as st
import pandas as pd
import numpy as np
from groq import Groq
import os
import matplotlib.pyplot as plt

# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="Smart Transportation AI",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 AI Smart Transportation System")
st.write("Optimize routes, predict traffic congestion, and improve transportation efficiency using AI.")

# ----------------------------
# Groq API Setup
# ----------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)

# ----------------------------
# Sidebar Inputs
# ----------------------------

st.sidebar.header("Vehicle & Route Information")

vehicle_id = st.sidebar.text_input("Vehicle ID")

start_location = st.sidebar.text_input("Start Location")

destination = st.sidebar.text_input("Destination")

distance = st.sidebar.slider("Distance (km)", 1, 500, 50)

traffic_level = st.sidebar.selectbox(
    "Traffic Condition",
    ["Low", "Medium", "High"]
)

weather = st.sidebar.selectbox(
    "Weather Condition",
    ["Clear", "Rain", "Storm", "Fog"]
)

fuel_consumption = st.sidebar.slider(
    "Fuel Consumption (liters)",
    1, 50, 10
)

delivery_time = st.sidebar.slider(
    "Delivery Time Constraint (minutes)",
    30, 600, 120
)

# ----------------------------
# Traffic Prediction Logic
# ----------------------------

def predict_congestion(traffic, weather):

    score = 0

    if traffic == "High":
        score += 3
    elif traffic == "Medium":
        score += 2
    else:
        score += 1

    if weather in ["Storm", "Fog"]:
        score += 2
    elif weather == "Rain":
        score += 1

    if score >= 4:
        return "High Congestion"
    elif score >= 3:
        return "Moderate Congestion"
    else:
        return "Low Congestion"


# ----------------------------
# Route Efficiency
# ----------------------------

def calculate_efficiency(distance, fuel):

    efficiency = distance / fuel

    if efficiency < 5:
        return "Low Efficiency"
    elif efficiency < 10:
        return "Moderate Efficiency"
    else:
        return "High Efficiency"


# ----------------------------
# Analyze Button
# ----------------------------

if st.button("Analyze Transportation Data"):

    congestion = predict_congestion(traffic_level, weather)

    efficiency = calculate_efficiency(distance, fuel_consumption)

    st.subheader("🚦 Congestion Prediction")

    if congestion == "High Congestion":
        st.error(congestion)
    elif congestion == "Moderate Congestion":
        st.warning(congestion)
    else:
        st.success(congestion)

    st.subheader("⛽ Fuel Efficiency")

    st.info(efficiency)

    # ----------------------------
    # Alerts
    # ----------------------------

    st.subheader("⚠ Transportation Alerts")

    if weather in ["Storm", "Fog"]:
        st.warning("Weather may cause delays or accidents.")

    if traffic_level == "High":
        st.warning("Heavy traffic detected. Route optimization recommended.")

    # ----------------------------
    # Visualization
    # ----------------------------

    st.subheader("📊 Traffic Visualization")

    data = pd.DataFrame({
        "Metric": ["Distance", "Fuel Used", "Delivery Time"],
        "Value": [distance, fuel_consumption, delivery_time]
    })

    st.bar_chart(data.set_index("Metric"))

    # ----------------------------
    # AI Recommendation using Groq
    # ----------------------------

    if client:

        prompt = f"""
        Transportation analysis for logistics.

        Vehicle ID: {vehicle_id}
        Start Location: {start_location}
        Destination: {destination}
        Distance: {distance} km
        Traffic Level: {traffic_level}
        Weather: {weather}
        Fuel Consumption: {fuel_consumption} liters
        Delivery Time Limit: {delivery_time} minutes
        Congestion Prediction: {congestion}

        Provide:
        - Route optimization suggestion
        - Traffic risk analysis
        - Fuel efficiency improvements
        - Safety recommendations
        """

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        ai_output = response.choices[0].message.content

        st.subheader("🤖 AI Transportation Recommendation")

        st.write(ai_output)

    else:
        st.warning("Groq API key not detected. AI recommendations disabled.")

# ----------------------------
# Fleet Management Demo Data
# ----------------------------

st.subheader("🚚 Fleet Management Overview")

fleet_data = pd.DataFrame({
    "Vehicle": ["Truck 1", "Truck 2", "Van 1", "Van 2"],
    "Fuel Used": np.random.randint(10, 40, 4),
    "Distance": np.random.randint(50, 300, 4),
    "Status": ["Active", "Active", "Delayed", "Active"]
})

st.dataframe(fleet_data)

st.write("This dashboard helps logistics managers monitor fleet performance.")