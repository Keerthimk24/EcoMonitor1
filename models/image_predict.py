import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# Initialize model variable
model = None

def load_inference_model():
    global model
    model_path = "saved_models/pollution_cnn.h5"
    if os.path.exists(model_path):
        model = load_model(model_path)
        print("Model loaded successfully.")
    else:
        print("Model file not found. Please run train_image_model.py first.")

def predict_pollution(img_path):
    global model
    if model is None:
        load_inference_model()
        if model is None:
            return "Model Error"

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    predictions = model.predict(img_array)
    class_idx = np.argmax(predictions[0])
    
    # Mapping based on the 6 folder structure seen in dataset
    # 0: a_Good, 1: b_Moderate (Low)
    # 2: c_Unhealthy..., 3: d_Unhealthy (Medium)
    # 4: e_Very_Unhealthy, 5: f_Severe (High)
    
    # Note: verify class indices from train_generator.class_indices if possible, 
    # but alphabetical order is standard for flow_from_directory.
    
    if class_idx == 0:
        return "Low Pollution"
    elif class_idx == 1:
        return "Moderate Pollution"
    elif class_idx in [2, 3]:
        return "High Pollution"
    else:
        return "Severe Pollution"

if __name__ == "__main__":
    # Test
    # print(predict_pollution("test_image.jpg"))
    pass
