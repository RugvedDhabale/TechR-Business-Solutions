# -*- coding: utf-8 -*-
"""final fakeface.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KSgDutSJMKk0Pf_YbxEGF8qakvbrYbx8
"""

!pip install gradio
import gradio as gr
import cv2
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

# Load pre-trained VGG16 model trained on imagenet without top classification layer
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze convolutional layers
for layer in base_model.layers:
    layer.trainable = False

# Add custom classification layers
x = Flatten()(base_model.output)
x = Dense(256, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)

# Create model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile model
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Define classes
classes = ['Real', 'Fake']

def classify_face(image):
    # Resize image to 224x224 (VGG16 input size)
    image = cv2.resize(image, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    # Predict class
    prediction = model.predict(image)[0, 0]
    label = classes[int(np.round(prediction))]
    return label

# Create Gradio interface
iface = gr.Interface(
    fn=classify_face,
    inputs="image",
    outputs="label",
    title="Fake Face Detector",
    description="Detects whether a face is real or fake.",

)

# Launch interface
iface.launch()