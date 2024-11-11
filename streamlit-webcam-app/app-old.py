import cv2
import streamlit as st

st.title("Webcam en tiempo real con OpenCV")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    st.error("No se pudo abrir la cámara")
else:
    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("No se pudo obtener el frame de la cámara")
            break

        # Convertir de BGR a RGB para mostrar en Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

cap.release()
