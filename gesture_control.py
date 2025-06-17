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

