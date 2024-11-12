import cv2
import numpy as np
import streamlit as st
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import tempfile

st.title("Detección de Frutas en Tiempo Real")

# Inicializar el estado de carga para modelo, etiquetas y cámara
if "model" not in st.session_state:
    st.session_state["model"] = None
if "etiquetas_invertidas" not in st.session_state:
    st.session_state["etiquetas_invertidas"] = None
if "camera_active" not in st.session_state:
    st.session_state["camera_active"] = False

# Opciones de carga en la barra lateral
st.sidebar.header("Opciones de Carga")

# 1. Cargar el modelo en la barra lateral (si no está en session_state)
st.sidebar.subheader("Paso 1: Cargar el Modelo")
modelo_archivo = st.sidebar.file_uploader("Carga tu archivo de modelo (.h5)", type=["h5"])

if modelo_archivo is not None and st.session_state["model"] is None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".h5") as temp_file:
        temp_file.write(modelo_archivo.read())
        st.session_state["model"] = load_model(temp_file.name, compile=False)
    st.sidebar.success("Modelo cargado exitosamente.")

# 2. Cargar las etiquetas de clase en la barra lateral (si no están en session_state)
st.sidebar.subheader("Paso 2: Cargar las Etiquetas de Clase")
etiquetas_archivo = st.sidebar.file_uploader("Carga el archivo de etiquetas (.npy)", type=["npy"])

if etiquetas_archivo is not None and st.session_state["etiquetas_invertidas"] is None:
    etiqueta_clase = np.load(etiquetas_archivo, allow_pickle=True).item()
    st.session_state["etiquetas_invertidas"] = {v: k for k, v in etiqueta_clase.items()}
    st.sidebar.success("Etiquetas cargadas exitosamente.")

# Umbral de confianza para mostrar el recuadro
CONFIDENCE_THRESHOLD = 80.0

# Botones de iniciar y detener
if st.sidebar.button("Iniciar Cámara"):
    st.session_state["camera_active"] = True
if st.sidebar.button("Detener Cámara"):
    st.session_state["camera_active"] = False

# Iniciar la cámara solo si el modelo y etiquetas están cargados y la cámara está activa
if st.session_state["model"] is not None and st.session_state["etiquetas_invertidas"] is not None:
    if st.session_state["camera_active"]:
        st.header("Detección en Tiempo Real Iniciada")

        # Configuración de la cámara
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        # Bucle para capturar los fotogramas de la cámara en tiempo real
        while cap.isOpened() and st.session_state["camera_active"]:
            ret, frame = cap.read()
            if not ret:
                st.error("No se pudo obtener la imagen de la cámara.")
                break

            # Preprocesar el fotograma para el modelo
            img = cv2.resize(frame, (64, 64))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0  # Normalizar

            # Realizar la predicción
            predicciones = st.session_state["model"].predict(img_array)
            indice_clase = np.argmax(predicciones)
            porcentaje_prediccion = predicciones[0][indice_clase] * 100
            fruta_predicha = st.session_state["etiquetas_invertidas"][indice_clase]

            # Si la confianza es mayor que el umbral, detecta el contorno del objeto
            if porcentaje_prediccion >= CONFIDENCE_THRESHOLD:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (15, 15), 0)
                edges = cv2.Canny(blurred, 30, 150)
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Si se encuentran contornos, dibujar el cuadro alrededor del contorno más grande
                if contours:
                    largest_contour = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(largest_contour)

                    # Dibujar el cuadro delimitador y la etiqueta
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    texto = f'{fruta_predicha} ({porcentaje_prediccion:.2f}%)'
                    cv2.putText(frame, texto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Convertir de BGR a RGB para mostrar en Streamlit
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame, channels="RGB")

        # Liberar la cámara cuando se detiene o al terminar
        cap.release()
    else:
        st.warning("La cámara está desactivada. Presiona 'Iniciar Cámara' para empezar la detección.")
else:
    st.warning("Por favor, carga un modelo y etiquetas para empezar la detección.")
