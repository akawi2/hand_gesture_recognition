import tkinter as tk
from tkinter import Canvas, Frame, Label, Button, filedialog, messagebox
import subprocess
import threading
import os


# Gradient function
def draw_linear_gradient(canvas, width, height, colors, angle=135):
    steps = height  # Nombre de bandes verticales pour un dégradé fluide
    rgb_colors = [tuple(int(c.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) for c in colors]
    gradient_colors = []

    # Interpolate colors vertically
    for i in range(steps):
        fraction = i / (steps - 1) if steps > 1 else 0
        r = int(rgb_colors[0][0] + sum(
            (rgb_colors[j + 1][0] - rgb_colors[j][0]) * (fraction ** (len(colors) - 1 - j)) for j in
            range(len(colors) - 1)))
        g = int(rgb_colors[0][1] + sum(
            (rgb_colors[j + 1][1] - rgb_colors[j][1]) * (fraction ** (len(colors) - 1 - j)) for j in
            range(len(colors) - 1)))
        b = int(rgb_colors[0][2] + sum(
            (rgb_colors[j + 1][2] - rgb_colors[j][2]) * (fraction ** (len(colors) - 1 - j)) for j in
            range(len(colors) - 1)))
        gradient_colors.append(f"#{r:02x}{g:02x}{b:02x}")

    # Fill the canvas with gradient rectangles
    for i in range(steps):
        canvas.create_rectangle(0, i * height // steps, width, (i + 1) * height // steps,
                                fill=gradient_colors[i], outline=gradient_colors[i])


# Modern Button class
class ModernButton(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = kwargs.get('bg', '#FF4081')
        self.hover_bg = '#E91E63'
        self.config(
            relief='flat',
            borderwidth=0,
            font=("Montserrat", 14, "bold"),
            fg='white',
            activebackground=self.hover_bg,
            activeforeground='white',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(bg=self.hover_bg)

    def on_leave(self, e):
        self.config(bg=self.default_bg)


# Main Application
class GestureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GestureSync")
        self.geometry("800x500")
        self.resizable(False, False)

        self.gradient_colors = ["#6B48FF", "#FF69B4", "#FF8E53", "#40C4FF", "#D81B60"]

        self.frames = {}
        for F in (WelcomePage, ModelSelectionPage, NotAvailablePage):
            page = F(parent=self, controller=self)
            self.frames[F] = page
            page.place(relwidth=1, relheight=1)
        self.show_frame(WelcomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


# Page 1: Welcome Page
class WelcomePage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        canvas = Canvas(self, width=800, height=500, highlightthickness=0)  # Removed bg='transparent'
        canvas.place(relwidth=1, relheight=1)
        draw_linear_gradient(canvas, 800, 500, controller.gradient_colors)
        Label(self, text="Welcome to Hand Gesture Application✨",
              font=("Raleway", 28, "bold"), bg="#6B48FF", fg="#F5F5F5").pack(pady=50)
        Label(self, text="Control your presentations with intuitive hand gestures.😄",
              font=("Roboto", 18), bg="#6B48FF",fg="#F5F5F5").pack(pady=5)
        ModernButton(self, text="Get Started", bg="#FF4081",
                     command=lambda: controller.show_frame(ModelSelectionPage)).pack(pady=120)


# Page 2: Model Selection
class ModelSelectionPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        canvas = Canvas(self, width=800, height=500, highlightthickness=0)  # Removed bg='transparent'
        canvas.place(relwidth=1, relheight=1)
        draw_linear_gradient(canvas, 800, 500, controller.gradient_colors)

        Label(self, text="Select Your Gesture Model🪼",
              font=("Montserrat", 24, "bold"), bg="#6B48FF", fg="#F5F5F5").pack(pady=80)
        ModernButton(self, text="CNN-Based Model", width=25, bg="#3F51B5",
                     command=self.launch_cnn_model).pack(pady=20)
        ModernButton(self, text="MediaPipe-Based Model", width=25, bg="#FF69B4",
                     command=self.launch_mediapipe_model).pack(pady=20)
        ModernButton(self, text="Back to Home", bg="#FF5722", width=25,
                     command=lambda: controller.show_frame(WelcomePage)).pack(pady=30)

    def launch_cnn_model(self):
        filepath = filedialog.askopenfilename(filetypes=[("PowerPoint files", "*.pptx *.ppsx")])
        if not filepath:
            messagebox.showwarning("No File Selected", "Please choose a PowerPoint file to continue.")
            return

        try:
            subprocess.Popen(['start', '', filepath], shell=True)
            messagebox.showinfo("Presentation Launched",
                                "Your presentation is open. Switch to slideshow mode to start gesturing!")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Could not open the file: {e}")
            return

        def run_gesture_detection():
            os.system("python realtime_test.py")

        detection_thread = threading.Thread(target=run_gesture_detection)
        detection_thread.daemon = True
        detection_thread.start()

    def launch_mediapipe_model(self):
        filepath = filedialog.askopenfilename(filetypes=[("PowerPoint files", "*.pptx *.ppsx")])
        if not filepath:
            messagebox.showwarning("No File Selected", "Please choose a PowerPoint file to continue.")
            return

        try:
            subprocess.Popen(['start', '', filepath], shell=True)
            messagebox.showinfo("Presentation Launched",
                                "Your presentation is open. Switch to slideshow mode to start gesturing!")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Could not open the file: {e}")
            return

        def run_gesture_detection():
            os.system("python realtime.py")


        detection_thread = threading.Thread(target=run_gesture_detection)
        detection_thread.daemon = True
        detection_thread.start()


# Page 3: Not Available Info
class NotAvailablePage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        canvas = Canvas(self, width=800, height=500, highlightthickness=0)  # Removed bg='transparent'
        canvas.place(relwidth=1, relheight=1)
        draw_linear_gradient(canvas, 800, 500, controller.gradient_colors)

        Label(self, text="MediaPipe Model Coming Soon",
              font=("Montserrat", 24, "bold"), fg="#FFFFFF").pack(pady=120)
        Label(self, text="This feature is in development. Stay tuned!",
              font=("Roboto", 18), fg="#F5F5F5").pack(pady=10)
        ModernButton(self, text="Back to Selection", bg="#FF5722", width=20,
                     command=lambda: controller.show_frame(ModelSelectionPage)).pack(pady=60)


# Launch the app
if __name__ == "__main__":
    app = GestureApp()
    app.mainloop()














# import tkinter as tk
# from tkinter import filedialog, messagebox
# import os
# import subprocess
# import threading
#
# # Fonction pour lancer PowerPoint et la détection
# def start_presentation():
#     filepath = filedialog.askopenfilename(filetypes=[("PowerPoint files", "*.pptx *.ppsx")])
#     if not filepath:
#         messagebox.showwarning("Warning", "No PowerPoint file selected.")
#         return
#
#     # Lancer le fichier PowerPoint (Windows uniquement)
#     try:
#         subprocess.Popen(['start', '', filepath], shell=True)
#         messagebox.showinfo("Info", "Presentation started. Please switch to slideshow mode.")
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to open PowerPoint file: {e}")
#         return
#
#     # Lancer le script de détection des gestes dans un thread
#     def run_gesture_detection():
#         os.system("python realtime_test.py")  # Assure-toi que real-time.py est prêt
#
#     detection_thread = threading.Thread(target=run_gesture_detection)
#     detection_thread.daemon = True  # Le thread se termine quand la fenêtre se ferme
#     detection_thread.start()
#
# # Création de l’interface Tkinter
# window = tk.Tk()
# window.title("Hand Gesture Controlled Presentation")
# window.geometry("500x200")
# window.resizable(False, False)
#
# title = tk.Label(window, text="Gesture-Controlled PowerPoint Launcher", font=("Helvetica", 16, "bold"))
# title.pack(pady=20)
#
# start_btn = tk.Button(window, text="Upload PowerPoint and Start Detection", command=start_presentation, bg="#007ACC", fg="white", font=("Helvetica", 12), width=40)
# start_btn.pack(pady=10)
#
# info = tk.Label(window, text="Note: Use predefined hand gestures to control the slides.", fg="gray")
# info.pack(pady=10)
#
# window.mainloop()
