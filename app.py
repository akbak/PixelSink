import os
import json
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Analiz modüllerini import et
from analyzer.hash_generator import generate_sha256, generate_phash
from analyzer.exif_reader import read_exif_data
from analyzer.lsb_detector import detect_lsb_steganography

# Flask uygulamasını başlat
app = Flask(__name__)

# Konfigürasyon
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
app.config['SECRET_KEY'] = 'supersecretkey'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Klasörlerin varlığını kontrol et
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)

        # Analizleri çalıştır
        sha256_hash = generate_sha256(file_path)
        phash = generate_phash(file_path)
        exif_data = read_exif_data(file_path)
        lsb_analysis = detect_lsb_steganography(file_path)

        # Şüpheli skor hesapla
        suspicion_score = 0
        if exif_data and exif_data.get('Status') != 'No EXIF information found.':
            suspicion_score += 10
            # GPS verisi özellikle şüpheli
            if any('GPS' in key for key in exif_data.keys()):
                suspicion_score += 20
        
        if lsb_analysis.get('suspicion_level') == 'High':
            suspicion_score += 40

        # Sonuçları topla
        results = {
            'image_path': new_filename,
            'sha256': sha256_hash,
            'phash': phash,
            'exif_data': exif_data,
            'lsb_analysis': lsb_analysis,
            'suspicion_score': suspicion_score
        }

        return render_template('report.html', results=results)

    else:
        flash('Invalid file type. Only PNG, JPG, JPEG are allowed.')
        return redirect(url_for('index'))

# Yüklenen dosyaları sunmak için bir route
from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
