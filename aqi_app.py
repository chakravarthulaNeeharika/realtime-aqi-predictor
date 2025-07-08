import streamlit as st
import pandas as pd
import requests
import joblib
import geocoder
import os
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()

# Load model
model = joblib.load("aqi_model.pkl")

# 🌐 API keys from environment
GEOAPIFY_KEY = os.getenv("GEOAPIFY_API_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

# 📍 Geocoding using Geoapify
def get_coordinates(city_name):
    url = f"https://api.geoapify.com/v1/geocode/search?text={city_name}&apiKey={GEOAPIFY_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        res = response.json()
        if res["features"]:
            coords = res["features"][0]["properties"]
            return {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "city": coords["city"] or city_name
            }
    return None

# 🌐 Auto location (IP-based)
def get_location_ip():
    g = geocoder.ip("me")
    if g.ok:
        return {
            "latitude": g.latlng[0],
            "longitude": g.latlng[1],
            "city": g.city or "Your Area"
        }
    return None

# 🌦️ Get weather data
def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"]
        }
    return None

# 🧠 Predict PM2.5
def predict_pm25(aod, temp, humidity, windspeed):
    input_df = pd.DataFrame([[aod, temp, humidity, windspeed]],
                            columns=["AOD", "Temperature", "Humidity", "WindSpeed"])
    return model.predict(input_df)[0]

# 🚀 Streamlit UI
st.set_page_config(page_title="🌫️ Real-Time AQI Predictor", layout="centered")
st.title("🌍 Real-Time PM2.5 Predictor")

method = st.radio("📌 How do you want to provide location?", ["🌐 Auto (IP-based)", "📝 Manual (Type a city)"])

if method == "📝 Manual (Type a city)":
    city_input = st.text_input("🌆 Enter a city name:")
    if city_input and st.button("🔍 Predict AQI"):
        with st.spinner("Getting location and weather..."):
            location = get_coordinates(city_input)
            if location:
                weather = get_weather(location["latitude"], location["longitude"])
                if weather:
                    aod = 0.6  # 🔧 Placeholder for AOD
                    prediction = predict_pm25(aod, weather["temperature"], weather["humidity"], weather["wind"])
                    st.success(f"📍 Location: {location['city']}")
                    st.markdown(f"### 💨 Predicted PM2.5: `{prediction:.2f} µg/m³`")
                    st.markdown(f"- 🌡️ Temp: `{weather['temperature']} °C`\n- 💧 Humidity: `{weather['humidity']} %`\n- 🌬️ Wind Speed: `{weather['wind']} m/s`")
                else:
                    st.error("❌ Couldn’t fetch weather.")
            else:
                st.error("❌ City not found.")
else:
    if st.button("📍 Auto-detect and Predict"):
        with st.spinner("Locating you via IP..."):
            location = get_location_ip()
            if location:
                weather = get_weather(location["latitude"], location["longitude"])
                if weather:
                    aod = 0.6
                    prediction = predict_pm25(aod, weather["temperature"], weather["humidity"], weather["wind"])
                    st.success(f"📍 Location: {location['city']}")
                    st.markdown(f"### 💨 Predicted PM2.5: `{prediction:.2f} µg/m³`")
                    st.markdown(f"- 🌡️ Temp: `{weather['temperature']} °C`\n- 💧 Humidity: `{weather['humidity']} %`\n- 🌬️ Wind Speed: `{weather['wind']} m/s`")
                else:
                    st.error("❌ Weather data failed.")
            else:
                st.error("❌ IP location not available.")

