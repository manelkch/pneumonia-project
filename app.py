from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Chargement du modèle CNN
MODEL_PATH = 'pneumonia_cnn.h5'
model = tf.keras.models.load_model(MODEL_PATH)

def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array / 255.0

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier envoyé'}), 400
    
    file = request.files['file']
    file_path = "temp_image.jpg"
    file.save(file_path)
    
    # Prédiction
    prepared_img = prepare_image(file_path)
    prediction = model.predict(prepared_img)
    
    # Nettoyage
    os.remove(file_path)
    
    result = "Pneumonie" if prediction[0][0] > 0.5 else "Sain"
    return jsonify({
        'prediction': result,
        'probability': float(prediction[0][0])
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'model_loaded': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)