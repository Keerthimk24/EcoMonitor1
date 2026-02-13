
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

def debug_predict(img_path):
    model_path = "saved_models/pollution_cnn.h5"
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        return

    try:
        model = load_model(model_path)
        print("Model loaded.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    predictions = model.predict(img_array)
    class_idx = np.argmax(predictions[0])
    
    print(f"Permissions: {predictions[0]}")
    print(f"Class Index: {class_idx}")
    
    # Mapping
    from models.image_predict import predict_pollution
    result = predict_pollution(img_path)
    print(f"Prediction Result: {result}")

if __name__ == "__main__":
    debug_predict("static/uploads/SMOKE.jpg")
