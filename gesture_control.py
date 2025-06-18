# gesture_control.py
import cv2
import mediapipe as mp
import pyautogui
import joblib

# Charger ton modèle entraîné (SVM ou CNN)
model = joblib.load("mon_modele.pkl")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            landmarks = []
            for lm in hand.landmark:
                landmarks.extend([lm.x, lm.y])

            # Prédiction
            gesture = model.predict([landmarks])[0]

            if gesture == "swipe_right":
                pyautogui.press("right")
            elif gesture == "swipe_left":
                pyautogui.press("left")

    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
