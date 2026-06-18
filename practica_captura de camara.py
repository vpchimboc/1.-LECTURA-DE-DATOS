#practica captura de camara mostrar en tiempo real el video de la camara utilizando streamlit y opencv
import streamlit as st
import cv2
st.title("Práctica: Captura de cámara en tiempo real")
#capturar video de la camara siempre y cuando presione el boton de iniciar captura
if st.button("Iniciar captura"):
    cap = cv2.VideoCapture(0)
   
    ret, frame = cap.read()
    if not ret:
        st.error("No se pudo capturar video")
        cap.release()
    #mostrar el video en streamlit
    st.image(frame, channels="BGR")
    cap.release()
#Reconocer el rostro de una persona utilizando opencv y mostrar un mensaje de bienvenida
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
if st.button("Reconocer rostro"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        st.error("No se pudo capturar video")
        cap.release()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    st.image(frame, channels="BGR")
    if len(faces) > 0:
        st.success("¡Bienvenido!")
    else:
        st.warning("No se detectó ningún rostro")
    cap.release()


