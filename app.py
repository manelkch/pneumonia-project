import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Chargement du modèle
model = tf.keras.models.load_model('pneumonia_cnn.h5')

def prepare_image(file):
    img = Image.open(file)
    # Conversion en niveaux de gris
    img = ImageOps.grayscale(img)
    # Redimensionnement à 150x150
    img = img.resize((150, 150))
    # Normalisation et conversion array
    img_array = np.array(img) / 255.0
    # Reshape pour le modèle : (1, 150, 150, 1)
    prepared_img = img_array.reshape(1, 150, 150, 1).astype(np.float32)
    return prepared_img

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
   
    file = request.files['file']
    try:
        prepared_img = prepare_image(file)
        prediction = model.predict(prepared_img)
       
        # Class 0 = Pneumonia, Class 1 = Normal
        prob = float(prediction[0][0])
        label = "NORMAL" if prob > 0.5 else "PNEUMONIA"

        return jsonify({
            'prediction': label,
            'probability': prob,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'OK', 'model_loaded': True})
    
@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
