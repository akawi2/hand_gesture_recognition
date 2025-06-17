import os
import cv2
import numpy as np
import mediapipe as mp
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Function to plot confusion matrix
def plot_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix for Gesture Recognition')
    plt.show()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Function to extract landmarks from an image
def extract_landmarks(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]  # Take the first detected hand
        return np.array([landmark.x for landmark in landmarks.landmark] +
                        [landmark.y for landmark in landmarks.landmark])
    return None

# Load dataset
dataset_path = 'dataset/'
X = []
y = []

for gesture in os.listdir(dataset_path):
    gesture_path = os.path.join(dataset_path, gesture)
    if os.path.isdir(gesture_path):
        for image_name in os.listdir(gesture_path):
            image_path = os.path.join(gesture_path, image_name)
            image = cv2.imread(image_path)
            landmarks = extract_landmarks(image)
            if landmarks is not None:
                X.append(landmarks)
                y.append(gesture)

# Convert to NumPy arrays
X = np.array(X)
y = np.array(y)

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Model file path
model_file = 'gesture_recognition_model.pkl'

if os.path.exists(model_file):
    # Load the model if it exists
    model = joblib.load(model_file)
    print('Model loaded')
else:
    # Train the SVM model
    model = SVC(kernel='linear')
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, model_file)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')



    # Evaluate and visualize results
    gesture_labels = sorted(le.classes_)  # Get gesture names from LabelEncoder

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    print("Classification Report:\n", classification_report(y_test, y_pred, target_names=gesture_labels))

    plot_confusion_matrix(y_test, y_pred, labels=gesture_labels)
