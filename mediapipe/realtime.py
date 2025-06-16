# import cv2
# import mediapipe as mp
# import numpy as np
# from sklearn.preprocessing import LabelEncoder
# import joblib
# import os

# # Initialiser MediaPipe
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()


# # Fonction pour extraire les landmarks d'une image
# def extract_landmarks(image):
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = hands.process(image_rgb)

#     if results.multi_hand_landmarks:
#         landmarks = results.multi_hand_landmarks[0]  # Prendre la première main
#         return np.array([landmark.x for landmark in landmarks.landmark] +
#                         [landmark.y for landmark in landmarks.landmark])
#     return None

# le = LabelEncoder()

# model_file = 'gesture_recognition_model.pkl'
# if os.path.exists(model_file):
#     # Charger le modèle si le fichier existe
#     model = joblib.load(model_file)
#     print('Model loaded')

#     # Pour une nouvelle image
#     #new_image = cv2.imread("test4.jpeg")
#     #new_landmarks = extract_landmarks(new_image)
#     # Capture vidéo
#     cap = cv2.VideoCapture(0)  # 0 pour la webcam

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Traitement de l'image
#         image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = hands.process(image_rgb)

#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 # Extraire les caractéristiques
#                 landmarks = extract_landmarks(hand_landmarks)

#                 # Prédire le geste
#                 prediction = model.predict([landmarks])
#                 gesture = prediction[0]  # Supposer que vous avez déjà mappé les étiquettes

#                 # Afficher le geste prédit sur l'image
#                 cv2.putText(frame, f'Geste: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

#                 # Dessiner les landmarks
#                 mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#         # Afficher le flux vidéo
#         cv2.imshow("Hand Gesture Recognition", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     """
#     if new_landmarks is not None:
#         prediction = model.predict([new_landmarks])
#         predicted_gesture = le.inverse_transform(prediction)
#         print(predicted_gesture)
#         print(f'Predicted Gesture: {predicted_gesture[0]}')
    
#     """


import cv2
import mediapipe as mp
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Initialiser MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Fonction pour extraire les landmarks d'une main
def extract_landmarks(hand_landmarks):
    return np.array([landmark.x for landmark in hand_landmarks.landmark] +
                    [landmark.y for landmark in hand_landmarks.landmark])

# le = LabelEncoder()

model_file = 'gesture_recognition_model.pkl'
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