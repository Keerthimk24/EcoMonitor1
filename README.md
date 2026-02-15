EcoMonitor1 is a comprehensive environment monitoring system built using the Air Pollution Image Dataset from India and Nepal (Kaggle). The system integrates image-based pollution classification, AQI prediction from pollutant sensor data, and report analysis into a unified Flask web application.

The platform supports pollution level detection, air quality prediction, and interactive dashboard visualization for monitoring environmental conditions.

📊 Dataset
Air Pollution Image Dataset (India & Nepal – Kaggle)

Total Images: 12,240

AQI Classes (6):

Good

Moderate

Unhealthy for Sensitive Groups

Unhealthy

Very Unhealthy

Severe

CSV Pollutant Data Includes:

PM2.5

PM10

CO

SO₂

NO₂

O₃

AQI

🛠️ Technologies Used
Component	Technology
Web Framework	Flask (Python)
Database	PostgreSQL
Image Model	TensorFlow / Keras (CNN)
Tabular Model	Scikit-learn
Model Explainability	LIME
Frontend	HTML / CSS / JavaScript
🤖 Models Developed

pollution_cnn.h5
Convolutional Neural Network (CNN) for image-based air pollution classification.

aqi_model.pkl
Machine learning model for AQI prediction based on pollutant concentration values.

LIME_20240506.best.hdf5
Optimized model integrated with LIME for interpretability and prediction explanation.

🚀 Application Features
1️⃣ Image-Based Pollution Classification

Upload an environmental image → System predicts pollution level (6 AQI categories).

2️⃣ AQI Prediction from Sensor Data

Input pollutant values (PM2.5, PM10, CO, SO₂, NO₂, O₃) → Predicts AQI level.

3️⃣ Text Report Analysis

Keyword-based NLP system for analyzing pollution-related reports.

4️⃣ Interactive Dashboard

Visual charts

Pollution distribution insights

Data-driven environmental monitoring

🎯 Key Capabilities

Multi-modal prediction (Image + Sensor Data)

Pollution severity classification

Explainable predictions using LIME

Web-based monitoring interface

Structured database integration (PostgreSQL)

🏗️ System Type

A complete Environment Monitoring and Air Quality Assessment System combining computer vision, data-driven AQI prediction, and web-based visualization.
