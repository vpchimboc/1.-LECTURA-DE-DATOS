import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import Label, Frame, Text, Scrollbar
from PIL import Image, ImageTk
import os

# Inicialización de MediaPipe
mp_hands = mp.solutions.hands
# Usamos static_image_mode=False para video en tiempo real
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Configuración de la ventana principal
root = tk.Tk()
root.title("Detector de Manos - Versión Estable")
root.state("zoomed")
root.configure(bg="#f0f2f5")

# --- ESTILOS ---
COLOR_BG = "#f0f2f5"
COLOR_HEADER = "#004d40"
COLOR_TEXT_HEADER = "white"
COLOR_DATA_PANEL = "#e0f2f1"

# --- ESTRUCTURA DE LA INTERFAZ ---
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=9)

# 1. ENCABEZADO
frame_header = Frame(root, bg=COLOR_HEADER, pady=10)
frame_header.grid(row=0, column=0, sticky="nsew")

Label(frame_header, text="DETECCIÓN DE MANOS", font=("Helvetica", 24, "bold"), 
      bg=COLOR_HEADER, fg=COLOR_TEXT_HEADER).pack()
Label(frame_header, text="Tecnología Superior en Big Data", font=("Helvetica", 14), 
      bg=COLOR_HEADER, fg=COLOR_TEXT_HEADER).pack()

# 2. SECCIÓN CENTRAL
frame_middle = Frame(root, bg=COLOR_BG)
frame_middle.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
frame_middle.columnconfigure(0, weight=1)
frame_middle.columnconfigure(1, weight=1)
frame_middle.rowconfigure(0, weight=1)

# Panel Cámara
frame_cam = Frame(frame_middle, bg="black", bd=2, relief="groove")
frame_cam.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
label_video = Label(frame_cam, bg="black")
label_video.pack(fill=tk.BOTH, expand=True)

# Panel Datos
frame_data = Frame(frame_middle, bg=COLOR_DATA_PANEL, bd=2, relief="groove")
frame_data.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

Label(frame_data, text="Monitor de Coordenadas", font=("Helvetica", 14, "bold"), 
      bg=COLOR_DATA_PANEL).pack(pady=5)

data_text = Text(frame_data, wrap="word", bg=COLOR_DATA_PANEL, font=("Consolas", 10), bd=0)
data_text.pack(side="left", fill="both", expand=True, padx=10)

scrollbar = Scrollbar(frame_data, command=data_text.yview)
scrollbar.pack(side="right", fill="y")
data_text.config(yscrollcommand=scrollbar.set)

# --- LÓGICA UNIFICADA ---
cap = cv2.VideoCapture(0)

def process_frame():
    ret, frame = cap.read()
    if ret:
        # 1. Preparar imagen
        frame = cv2.flip(frame, 1)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 2. Procesar con MediaPipe (UN SOLO LLAMADO)
        # Esto evita el error de "Packet timestamp mismatch"
        results = hands.process(rgb_image)
        
        # 3. Dibujar y extraer datos
        landmarks_info = ""
        if results.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Info de la mano detectada
                label = results.multi_handedness[i].classification[0].label
                landmarks_info += f"MANO: {label}\n"
                
                # Puntos principales
                for id, lm in enumerate(hand_landmarks.landmark):
                    # Solo mostrar puntos clave para no saturar el panel (Muñeca, puntas de dedos)
                    if id in [0, 4, 8, 12, 16, 20]:
                        name = ["Muñeca", "Pulgar", "Índice", "Medio", "Anular", "Meñique"][ [0,4,8,12,16,20].index(id) ]
                        landmarks_info += f"{name}: X={lm.x:.2f}, Y={lm.y:.2f}\n"
                landmarks_info += "-"*20 + "\n"

        # 4. Actualizar Interfaz
        # Actualizar Video
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        w = label_video.winfo_width()
        h = label_video.winfo_height()
        if w > 10 and h > 10:
            img = img.resize((w, h), Image.Resampling.LANCZOS)
        
        imgtk = ImageTk.PhotoImage(image=img)
        label_video.imgtk = imgtk
        label_video.configure(image=imgtk)

        # Actualizar Texto
        data_text.delete(1.0, tk.END)
        if landmarks_info:
            data_text.insert(tk.END, landmarks_info)
        else:
            data_text.insert(tk.END, "Esperando detección...\n")

    # Re-programar siguiente frame
    label_video.after(15, process_frame)

# Iniciar proceso
process_frame()

def on_closing():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()