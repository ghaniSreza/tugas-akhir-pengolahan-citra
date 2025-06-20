from flask import Flask, request, render_template, redirect, url_for, flash
import os
import joblib
import numpy as np
from werkzeug.utils import secure_filename
from utils import extract_glcm_features, allowed_file
import cv2

app = Flask(__name__)
app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load model dan scaler 
model, scaler = joblib.load('model_svm.pkl')

# Label fitur dari GLCM
feature_labels = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)

        # Ekstraksi fitur dari gambar
        features = extract_glcm_features(filepath)
        if features is None:
            flash("Ekstraksi fitur gagal")
            return redirect(url_for('index'))

        # Scaling fitur
        features_scaled = scaler.transform(features.reshape(1, -1))

        # Prediksi
        prediction = model.predict(features_scaled)[0]
        probas = model.predict_proba(features_scaled)[0]
        confidence = round(np.max(probas) * 100, 2)

        # Tampilkan fitur dalam tabel
        feature_data = [{"name": name, "value": round(val, 4)} for name, val in zip(feature_labels, features)]

        result = {
            'filename': filename,
            'prediction': prediction,
            'confidence': confidence,
            'features': feature_data
        }

        return render_template('result.html', result=result)
    else:
        flash("File tidak valid")
        return redirect(url_for('index'))

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True)
