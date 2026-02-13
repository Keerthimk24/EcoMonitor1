from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from werkzeug.utils import secure_filename
import psycopg2
import pickle
import numpy as np
from database.db_connection import get_db_connection, create_tables
from models.image_predict import predict_pollution
from models.nlp_model import predict_report
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change for production

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load AQI Model
AQI_MODEL_PATH = 'saved_models/aqi_model.pkl'
aqi_model = None
if os.path.exists(AQI_MODEL_PATH):
    with open(AQI_MODEL_PATH, 'rb') as f:
        aqi_model = pickle.load(f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def image_analysis():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Predict
            result = predict_pollution(filepath)
            
            # Save to DB
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO image_results (image_name, pollution_level) VALUES (%s, %s)", (filename, result))
                conn.commit()
                cur.close()
                conn.commit()
                cur.close()
                conn.close()
            else:
                flash("Database connection failed. Result not saved.", "error")
            
            return render_template('image.html', prediction=result, image_url=filepath)
    return render_template('image.html')

@app.route('/report', methods=['GET', 'POST'])
def report_analysis():
    if request.method == 'POST':
        report_text = request.form['report_text']
        issue_type = predict_report(report_text)
        
        # Save to DB
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO report_results (report_text, issue_type) VALUES (%s, %s)", (report_text, issue_type))
            conn.commit()
            cur.close()
            conn.close()
        else:
            flash("Database connection failed. Result not saved.", "error")
            
        return render_template('report.html', prediction=issue_type, report_text=report_text)
    return render_template('report.html')

@app.route('/prediction', methods=['GET', 'POST'])
def aqi_prediction():
    prediction = None
    if request.method == 'POST':
        try:
            # Inputs: CO, NO2, SO2, O3, PM2.5, PM10
            # User prompted: CO, NO2, Temperature, Humidity. 
            # I must use what the model was trained on: 'CO', 'NO2', 'SO2', 'O3', 'PM2.5', 'PM10'
            # If user form provides temp/humidity, I might ignore them or use dummy values if model expects them.
            # But earlier I trained the model on the available 6 columns.
            
            co = float(request.form.get('co', 0))
            no2 = float(request.form.get('no2', 0))
            so2 = float(request.form.get('so2', 0))
            o3 = float(request.form.get('o3', 0))
            pm25 = float(request.form.get('pm25', 0))
            pm10 = float(request.form.get('pm10', 0))
            
            if aqi_model:
                features = np.array([[co, no2, so2, o3, pm25, pm10]])
                prediction = aqi_model.predict(features)[0]
                
                # Save to DB
                conn = get_db_connection()
                if conn:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO aqi_results (predicted_aqi) VALUES (%s)", (prediction,))
                    conn.commit()
                    cur.close()
                    conn.close()
                else:
                    flash("Database connection failed. Result not saved.", "error")
            else:
                flash("AQI Model not loaded. Please train the model first.")
                
        except ValueError:
            flash("Invalid input values. Please enter numbers.")
            
    return render_template('prediction.html', prediction=prediction)

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    data = {}
    if conn:
        cur = conn.cursor()
        
        # 1. Pollution Distribution (Pie Chart) - from image_results
        cur.execute("SELECT pollution_level, COUNT(*) FROM image_results GROUP BY pollution_level")
        pollution_data = cur.fetchall()
        data['pollution_labels'] = [row[0] for row in pollution_data]
        data['pollution_counts'] = [row[1] for row in pollution_data]
        
        # 2. AQI Trend (Line Chart) - from aqi_results
        cur.execute("SELECT datetime, predicted_aqi FROM aqi_results ORDER BY datetime DESC LIMIT 10")
        aqi_data = cur.fetchall()
        # Sort by time asc for chart
        aqi_data.reverse()
        data['aqi_labels'] = [row[0].strftime("%Y-%m-%d %H:%M") for row in aqi_data]
        data['aqi_values'] = [row[1] for row in aqi_data]
        
        # 3. Report Issues (Bar Chart) - from report_results
        cur.execute("SELECT issue_type, COUNT(*) FROM report_results GROUP BY issue_type")
        report_data = cur.fetchall()
        data['report_labels'] = [row[0] for row in report_data]
        data['report_counts'] = [row[1] for row in report_data]
        
        # 4. Recent Activity (Table) - Combined/Union
        query = """
            SELECT id, 'Image' as type, pollution_level as result, datetime FROM image_results
            UNION ALL
            SELECT id, 'Report' as type, issue_type as result, datetime FROM report_results
            UNION ALL
            SELECT id, 'AQI' as type, CAST(predicted_aqi AS TEXT) as result, datetime FROM aqi_results
            ORDER BY datetime DESC LIMIT 10
        """
        cur.execute(query)
        recent_activity = cur.fetchall()
        
        data['recent_activity'] = recent_activity
        
        cur.close()
        conn.close()
    else:
        # Fallback empty data if DB connection fails
        data['pollution_labels'] = []
        data['pollution_counts'] = []
        data['aqi_labels'] = []
        data['aqi_values'] = []
        data['report_labels'] = []
        data['report_counts'] = []
        data['recent_activity'] = []
        flash("Database connection failed. Dashboard data may be incomplete.", "error")
    
    return render_template('dashboard.html', data=data)

# Init DB on start (optional, usually better to run script manually)
# create_tables()

if __name__ == '__main__':
    # Initialize DB tables if they don't exist
    create_tables()
    app.run(debug=True, port=5000)
