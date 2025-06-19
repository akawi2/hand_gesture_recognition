import pyautogui


def handle_ppt(confidence, class_names, predicted_class):
    if confidence > 0.8:  # pour éviter les fausses détections
        gesture = class_names[predicted_class]

        if gesture == "Defiler a droite":
            pyautogui.press("right")  # Slide suivante
        elif gesture == "Defiler a gauche":
            pyautogui.press("left")  # Slide précédente
        elif gesture == "Zoomer":
            pyautogui.hotkey("ctrl", "+")  # Zoomer
        elif gesture == "Dezoomer":
            pyautogui.hotkey("ctrl", "-")  # Dézoomer
        elif gesture == "Augmenter":
            pyautogui.press("volumeup")
        elif gesture == "Diminuer":
            pyautogui.press("volumedown")

def handle_ppt_svm(gesture, hand_landmarks=None):
    if gesture == "Gauche":
        pyautogui.press("right")  # Slide suivante
    elif gesture == "Droite":
        pyautogui.press("left")   # Slide précédente
    elif gesture == "Zoomer":
        pyautogui.hotkey("ctrl", "+")
    elif gesture == "Dezoomer":
        pyautogui.hotkey("ctrl", "-")
    elif gesture == "Augmenter":
        pyautogui.click(button='left')
    elif gesture == "Diminuer" and hand_landmarks is not None:
        index_finger = hand_landmarks.landmark[8]  # Index tip
        screen_w, screen_h = pyautogui.size()
        x = int(index_finger.x * screen_w)
        y = int(index_finger.y * screen_h)
        pyautogui.moveTo(x, y)