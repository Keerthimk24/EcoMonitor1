import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import os

# Configuration
DATASET_PATH = r"C:/Users/navee/Downloads/DLL/Air Pollution Image Dataset/Air Pollution Image Dataset/Combined_Dataset/IND_and_NEP"
MODEL_SAVE_PATH = "saved_models/pollution_cnn.h5"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5  # Reduced for quick testing, increase for real training

def train_model():
    print("Loading Base Model...")
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze base model layers
    for layer in base_model.layers:
        layer.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    # The dataset has 6 classes. We will train on 6 and map them to Low/Medium/High during prediction.
    predictions = Dense(6, activation='softmax')(x) 

    model = Model(inputs=base_model.input, outputs=predictions)

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    print("Preparing Data Generators...")
    # Using validation split since we don't have a separate test set structure provided for this specific path
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    train_generator = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    validation_generator = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    print("Starting Training...")
    model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // BATCH_SIZE,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // BATCH_SIZE,
        epochs=EPOCHS
    )

    # Ensure directory exists
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    
    print(f"Saving Model to {MODEL_SAVE_PATH}...")
    model.save(MODEL_SAVE_PATH)
    print("Model Saved!")

if __name__ == "__main__":
    train_model()
