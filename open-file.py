from tkinter import Canvas, Frame, Label, Button, filedialog, messagebox
import tkinter as tk
import subprocess
import threading
import os


#Color configuration
def draw_linear_gradient(canvas, width, height, colors):
    # Divise la hauteur en autant de bandes que de couleurs
    steps = len(colors) - 1
    band_height = height // steps

    for i in range(steps):
        r1, g1, b1 = canvas.winfo_rgb(colors[i])
        r2, g2, b2 = canvas.winfo_rgb(colors[i + 1])

        r_ratio = (r2 - r1) / band_height
        g_ratio = (g2 - g1) / band_height
        b_ratio = (b2 - b1) / band_height

        for j in range(band_height):
            nr = int(r1 + (r_ratio * j)) // 256
            ng = int(g1 + (g_ratio * j)) // 256
            nb = int(b1 + (b_ratio * j)) // 256
            color = f"#{nr:02x}{ng:02x}{nb:02x}"
            canvas.create_rectangle(0, i * band_height + j, width, i * band_height + j + 1, outline=color, fill=color)


# Main Application
class GestureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gesture-Controlled Presentation")
        self.geometry("700x400")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
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
        Frame.__init__(self, parent, bg="#003366")
        self.controller = controller



        Label(self, text="Welcome to the Gesture-Controlled Presentation System",
              font=("Helvetica", 18, "bold"), bg="#003366", fg="white").pack(pady=80)
        Label(self, text="Use hand gestures to control your PowerPoint slides.",
              font=("Helvetica", 14), bg="#003366", fg="white").pack(pady=10)
        Button(self, text="Start", font=("Helvetica", 14), bg="#00aaff", fg="white",
               command=lambda: controller.show_frame(ModelSelectionPage)).pack(pady=40)

# Page 2: Model Selection
class ModelSelectionPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#ffffff")
        self.controller = controller
        Label(self, text="Choose a Gesture Recognition Model",
              font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#003366").pack(pady=40)

        Button(self, text="CNN-Based Model", font=("Helvetica", 12), width=30,
               bg="#007ACC", fg="white", command=self.launch_cnn_model).pack(pady=10)

        Button(self, text="MediaPipe-Based Model", font=("Helvetica", 12), width=30,
               bg="#CCCCCC", fg="#666666", command=lambda: controller.show_frame(NotAvailablePage)).pack(pady=10)

        Button(self, text="Back to Welcome Page", font=("Helvetica", 10),
               command=lambda: controller.show_frame(WelcomePage)).pack(pady=30)

    def launch_cnn_model(self):
        filepath = filedialog.askopenfilename(filetypes=[("PowerPoint files", "*.pptx *.ppsx")])
        if not filepath:
            messagebox.showwarning("Warning", "No PowerPoint file selected.")
            return

        try:
            subprocess.Popen(['start', '', filepath], shell=True)
            messagebox.showinfo("Info", "Presentation started. Please switch to slideshow mode.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PowerPoint file: {e}")
            return

        def run_gesture_detection():
            os.system("python realtime_test.py")

        detection_thread = threading.Thread(target=run_gesture_detection)
        detection_thread.daemon = True
        detection_thread.start()

# Page 3: Not Available Info
class NotAvailablePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#FFDDDD")
        self.controller = controller
        Label(self, text="MediaPipe Model Not Yet Available",
              font=("Helvetica", 16, "bold"), bg="#FFDDDD", fg="#660000").pack(pady=80)
        Label(self, text="This feature is under development.",
              font=("Helvetica", 14), bg="#FFDDDD", fg="#660000").pack(pady=10)
        Button(self, text="Back to Model Selection", font=("Helvetica", 12),
               command=lambda: controller.show_frame(ModelSelectionPage)).pack(pady=40)

# Launch the app
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
