import threading
import tkinter as tk
from tkinter import filedialog
import os
import subprocess

# Fonction pour ouvrir un fichier PowerPoint
def open_ppt():
    filepath = filedialog.askopenfilename(filetypes=[("PowerPoint files", "*.pptx *.ppsx")])
    if filepath:
        # Lance PowerPoint en mode diaporama (Windows uniquement ici)
        subprocess.Popen(['start', '', filepath], shell=True)

# Interface Tkinter simple
window = tk.Tk()
window.title("Gesture-Controlled PowerPoint")
window.geometry("400x200")

label = tk.Label(window, text="Upload a PowerPoint File to Control with Gestures", wraplength=300)
label.pack(pady=20)

def start_presentation():
    filepath = filedialog.askopenfilename(filetypes=[("PowerPoint files", "*.pptx *.ppsx")])
    if filepath:
        # Lance PowerPoint
        subprocess.Popen(['start', '', filepath], shell=True)
        # Lance le script de reconnaissance dans un thread
        threading.Thread(target=lambda: os.system("python train.py")).start()

btn = tk.Button(window, text="Upload & Launch", command=start_presentation)

btn.pack()

window.mainloop()
