import cv2
import mediapipe as mp
import pyautogui

# Configuración de Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Configuración de la cámara
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Cambiar 0 por otro valor si es necesario

# Configuración de colores
color_mouse_pointer = (255, 0, 255)

# Tamaño de la pantalla (ajustar según la resolución de tu pantalla)
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Tamaño y ubicación del área de detección de gestos
SCREEN_GAME_X_INI = int(SCREEN_WIDTH * 0.2)
SCREEN_GAME_Y_INI = int(SCREEN_HEIGHT * 0.2)
SCREEN_GAME_X_FIN = int(SCREEN_WIDTH * 0.8)
SCREEN_GAME_Y_FIN = int(SCREEN_HEIGHT * 0.8)

aspect_ratio_screen = (SCREEN_GAME_X_FIN - SCREEN_GAME_X_INI) / (SCREEN_GAME_Y_FIN - SCREEN_GAME_Y_INI)

# Función para calcular la distancia euclidiana entre dos puntos
def calculate_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

# Función para detectar el gesto de clic (mano cerrada)
def detect_finger_closed(hand_landmarks):
    # Obtener las coordenadas de los puntos relevantes
    x_thumb = int(hand_landmarks.landmark[4].x * SCREEN_WIDTH)
    y_thumb = int(hand_landmarks.landmark[4].y * SCREEN_HEIGHT)
    x_index = int(hand_landmarks.landmark[8].x * SCREEN_WIDTH)
    y_index = int(hand_landmarks.landmark[8].y * SCREEN_HEIGHT)
    
    # Calcular la distancia entre el pulgar y el índice
    distance_thumb_index = calculate_distance(x_thumb, y_thumb, x_index, y_index)

    # Si la distancia es menor que un umbral, considerar como clic detectado
    if distance_thumb_index < 30:
        return True
    else:
        return False

# Inicializar Mediapipe Hands
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7) as hands:

    while True:
        # Capturar fotograma de la cámara
        ret, frame = cap.read()
        if not ret:
            break

        # Voltear el fotograma horizontalmente
        frame = cv2.flip(frame, 1)

        # Detección de gestos con Mediapipe Hands
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Procesar resultados si se detectan manos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujar puntos de referencia de la mano
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Obtener la posición del índice para controlar el cursor
                x = int(hand_landmarks.landmark[8].x * SCREEN_WIDTH)
                y = int(hand_landmarks.landmark[8].y * SCREEN_HEIGHT)

                # Mapear las coordenadas de la mano al área de la pantalla de la presentación
                xm = int(np.interp(x, (SCREEN_GAME_X_INI, SCREEN_GAME_X_FIN), (0, SCREEN_WIDTH)))
                ym = int(np.interp(y, (SCREEN_GAME_Y_INI, SCREEN_GAME_Y_FIN), (0, SCREEN_HEIGHT)))

                # Mover el cursor
                pyautogui.moveTo(xm, ym)

                # Detectar el gesto de clic (mano cerrada)
                if detect_finger_closed(hand_landmarks):
                    pyautogui.click()

        # Mostrar el fotograma con los resultados
        cv2.imshow('Hand Gestures for Presentation Control', frame)

        # Salir del bucle al presionar Esc
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
