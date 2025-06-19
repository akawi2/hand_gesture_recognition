
import time

import cv2
import mediapipe as mp
import numpy as np
import joblib
import os

from gesture_control import handle_ppt_svm

previous_gesture = None
gesture_start_time = 0
GESTURE_HOLD_DURATION = 0.7  # secondes

# Initialiser MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Fonction pour extraire les landmarks d'une main
def extract_landmarks(hand_landmarks):
    return np.array([landmark.x for landmark in hand_landmarks.landmark] +
                    [landmark.y for landmark in hand_landmarks.landmark])

# le = LabelEncoder()

model_file = 'mediapipe/gesture_recognition_model.pkl'
if os.path.exists(model_file):
    # Charger le modèle si le fichier existe
    model = joblib.load(model_file)
    print('Model loaded')

    # Capture vidéo
    cap = cv2.VideoCapture(0)  # 0 pour la webcam

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Traitement de l'image
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extraire les caractéristiques
                landmarks = extract_landmarks(hand_landmarks)

                # Prédire le geste
                prediction = model.predict([landmarks])
                # le = LabelEncoder()
                # print(prediction)
                gestures = ['Augmenter', 'Dezoomer', 'Diminuer', 'Droite', 'Gauche', 'Zoomer']
                gesture = prediction[0]#le.inverse_transform(prediction[0])  # Supposer que vous avez déjà mappé les étiquettes
                print("gesture value: ", gesture)

                # Mapping class → action PowerPoint
                current_time = time.time()

                if gesture == 2:
                    handle_ppt_svm(gesture, hand_landmarks)
                else:
                    if gesture == previous_gesture:
                        # même geste, vérifier depuis combien de temps
                        if current_time - gesture_start_time >= GESTURE_HOLD_DURATION:
                            handle_ppt_svm(gesture, hand_landmarks)
                            gesture_start_time = current_time  # éviter de répéter trop vite
                    else:
                        # Geste changé, redémarrer le chrono
                        previous_gesture = gesture
                        gesture_start_time = current_time

                # Afficher le geste prédit sur l'image
                cv2.putText(frame, f'Geste: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Dessiner les landmarks
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Afficher le flux vidéo
        cv2.imshow("Hand Gesture Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()