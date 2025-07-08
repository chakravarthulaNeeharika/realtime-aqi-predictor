# 🌫️ Real-Time AQI Predictor

A machine learning-powered web app that predicts **PM2.5 air quality** in real time using **AOD (Aerosol Optical Depth)**, weather data, and location detection.

## 🔍 Features

- 📍 Auto-location using IP or manual city input
- ☁️ Real-time weather data from OpenWeather
- 🔢 Predicts PM2.5 using trained ML model (Random Forest)
- 🧠 Easily customizable for any location worldwide
- 🌐 Built with Streamlit — no frontend needed

## 🚀 Tech Stack

- Python
- Streamlit
- scikit-learn
- OpenWeather API
- Geoapify API
- pandas, numpy, matplotlib, seaborn

## 🧠 Model Inputs

- AOD (simulated or replaceable with satellite input)
- Temperature (°C)
- Humidity (%)
- Wind Speed (m/s)

## 📦 How to Run

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/realtime-aqi-predictor.git
   cd realtime-aqi-predictor


TO run in jupyter notebook
save files as aqi_App.py and in terminal run it as 
"streamlit run aqi_app.py"
