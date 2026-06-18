import cv2
import numpy as np
import tkinter as tk
from tkinter import Label, Frame
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from deepface import DeepFace
import os
import time

# Configuración de la ventana principal
root = tk.Tk()
root.title("Detector de Emociones - Interfaz Equitativa")
root.state('zoomed')  # Iniciar maximizado
root.configure(bg='#f0f2f5')

# --- ESTILOS Y COLORES ---
COLOR_BG = '#f0f2f5'
COLOR_HEADER = '#e3f2fd'  # blanco azulado
COLOR_TEXT_HEADER = '#1a237e'
COLORS_EMOTIONS = {
    'happy': '#FFEB3B',     # Amarillo
    'angry': '#F44336',     # Rojo (Estrés)
    'sad': '#2196F3',       # Azul
    'surprised': '#FF9800', # Naranja
    'neutral': '#9E9E9E'    # Gris
}

# --- CONTENEDORES PRINCIPALES ---
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1) # Header
root.rowconfigure(1, weight=6) # Middle (Cámara e Histograma)
root.rowconfigure(2, weight=3) # Footer (Gráficos secundarios)

# 1. ENCABEZADO (Título, Subtítulo, Logo)
frame_header = Frame(root, bg=COLOR_HEADER, pady=10)
frame_header.grid(row=0, column=0, sticky="nsew")
frame_header.columnconfigure(0, weight=1)

title_label = Label(frame_header, text="DETECCIÓN DE EMOCIONES", font=("Helvetica", 28, "bold"), 
                    bg=COLOR_HEADER, fg=COLOR_TEXT_HEADER)
title_label.pack()

subtitle_label = Label(frame_header, text="Tecnología Superior en Big Data", font=("Helvetica", 16), 
                       bg=COLOR_HEADER, fg=COLOR_TEXT_HEADER)
subtitle_label.pack()

# Espacio para el logo (Carga segura)
try:
    # IMPORTANTE: Cambia esta ruta a la ubicación real de tu logo
    logo_path = r"D:\PROYECTOS PYTHON\RECONOCIMIENTO_FACIAL\LOGO.png"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((250, 80), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = Label(frame_header, image=logo_photo, bg=COLOR_HEADER)
        logo_label.image = logo_photo
        logo_label.pack(pady=5)
    else:
        Label(frame_header, text="[ LOGO ]", bg=COLOR_HEADER, fg="white", font=("Helvetica", 12)).pack()
except Exception:
    Label(frame_header, text="[ LOGO ]", bg=COLOR_HEADER, fg="white", font=("Helvetica", 12)).pack()

# 2. SECCIÓN CENTRAL (Cámara e Histograma 50/50)
frame_middle = Frame(root, bg=COLOR_BG)
frame_middle.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
frame_middle.columnconfigure(0, weight=1) # Cámara
frame_middle.columnconfigure(1, weight=1) # Histograma
frame_middle.rowconfigure(0, weight=1)

# Contenedor Cámara
frame_cam_container = Frame(frame_middle, bg="black", bd=2, relief="groove")
frame_cam_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
label_video = Label(frame_cam_container, bg="black")
label_video.pack(fill=tk.BOTH, expand=True)

# Contenedor Histograma Principal
frame_hist_container = Frame(frame_middle, bg="white", bd=2, relief="groove")
frame_hist_container.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

fig_main, ax_main = plt.subplots(figsize=(5, 4), dpi=100)
canvas_main = FigureCanvasTkAgg(fig_main, master=frame_hist_container)
canvas_main.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# 3. SECCIÓN INFERIOR (4 Gráficos de Pastel)
frame_footer = Frame(root, bg=COLOR_BG)
frame_footer.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
for i in range(4):
    frame_footer.columnconfigure(i, weight=1)
frame_footer.rowconfigure(0, weight=1)

fig_pies, axs_pie = plt.subplots(1, 4, figsize=(12, 3), dpi=90)
canvas_pies = FigureCanvasTkAgg(fig_pies, master=frame_footer)
canvas_pies.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- LÓGICA DE DETECCIÓN Y ACTUALIZACIÓN ---
cap = cv2.VideoCapture(0)
current_emotions = {'happy': 0, 'angry': 0, 'sad': 0, 'neutral': 0}

def update_ui(emotions):
    # Actualizar Histograma
    ax_main.clear()
    keys = list(emotions.keys())
    values = list(emotions.values())
    ax_main.bar(keys, values, color=[COLORS_EMOTIONS.get(k, '#E0E0E0') for k in keys])
    ax_main.set_title("Distribución de Emociones", fontsize=12, fontweight='bold')
    ax_main.set_ylim(0, 100)
    ax_main.set_ylabel("Porcentaje (%)")
    
    # Actualizar Pies
    titles = [('happy', '😊 Felicidad'), ('angry', '😠 Estrés'), 
              ('sad', '😢 Tristeza'), ('neutral', '😐 Neutral')]
    for i, (key, title) in enumerate(titles):
        axs_pie[i].clear()
        val = emotions.get(key, 0)
        axs_pie[i].pie([val, max(0.1, 100-val)], colors=[COLORS_EMOTIONS[key], '#eeeeee'], 
                       startangle=90, counterclock=False)
        axs_pie[i].set_title(title, fontsize=10, fontweight='bold')
        axs_pie[i].text(0, -1.2, f"{val:.1f}%", ha='center', fontsize=9)

    canvas_main.draw()
    canvas_pies.draw()

def analyze_frame():
    global current_emotions
    while True:
        ret, frame = cap.read()
        if ret:
            try:
                # Redimensionar para análisis rápido
                small_frame = cv2.resize(frame, (160, 120)) 
                res = DeepFace.analyze(small_frame, actions=['emotion'], enforce_detection=False, silent=True)
                if res:
                    raw_emotions = res[0]['emotion']
                    relevant = {k: raw_emotions.get(k, 0) for k in current_emotions.keys()}
                    total = sum(relevant.values())
                    if total > 0:
                        current_emotions = {k: (v/total)*100 for k, v in relevant.items()}
                    root.after(0, update_ui, current_emotions)
            except Exception as e:
                print(f"Error: {e}")
        time.sleep(1.5) # Analizar cada 1.5 segundos para balancear velocidad/carga

def show_video():
    ret, frame = cap.read()
    if ret:
        cv2_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2_img)
        
        w = label_video.winfo_width()
        h = label_video.winfo_height()
        if w > 10 and h > 10:
            img = img.resize((w, h), Image.Resampling.LANCZOS)
        
        imgtk = ImageTk.PhotoImage(image=img)
        label_video.imgtk = imgtk
        label_video.configure(image=imgtk)
    label_video.after(30, show_video)

# Iniciar hilos y bucles
threading.Thread(target=analyze_frame, daemon=True).start()
show_video()

# Manejo de cierre
def on_closing():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()