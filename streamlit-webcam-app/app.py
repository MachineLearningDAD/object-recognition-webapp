import cv2
import numpy as np
import streamlit as st
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from PIL import Image
import tempfile  # Para guardar archivos temporales

st.title("Detección de Frutas en Tiempo Real")

# Inicializar el estado de carga para modelo y etiquetas
if "model" not in st.session_state:
    st.session_state["model"] = None
if "etiquetas_invertidas" not in st.session_state:
    st.session_state["etiquetas_invertidas"] = None

# Opciones de carga en la barra lateral
st.sidebar.header("Opciones de Carga")

# 1. Cargar el modelo en la barra lateral
st.sidebar.subheader("Paso 1: Cargar el Modelo")
modelo_archivo = st.sidebar.file_uploader("Carga tu archivo de modelo (.h5)", type=["h5"])

if modelo_archivo is not None:
    # Guardar temporalmente el archivo cargado y luego cargar el modelo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".h5") as temp_file:
        temp_file.write(modelo_archivo.read())
        st.session_state["model"] = load_model(temp_file.name)
    st.sidebar.success("Modelo cargado exitosamente.")

# 2. Cargar las etiquetas de clase en la barra lateral
st.sidebar.subheader("Paso 2: Cargar las Etiquetas de Clase")
etiquetas_archivo = st.sidebar.file_uploader("Carga el archivo de etiquetas (.npy)", type=["npy"])

if etiquetas_archivo is not None:
    # Cargar las etiquetas de clase y almacenarlas en session_state
    etiqueta_clase = np.load(etiquetas_archivo, allow_pickle=True).item()
    st.session_state["etiquetas_invertidas"] = {v: k for k, v in etiqueta_clase.items()}
    st.sidebar.success("Etiquetas cargadas exitosamente.")

# Mostrar el botón de procesar solo si el modelo y las etiquetas están cargados
if st.session_state["model"] is not None and st.session_state["etiquetas_invertidas"] is not None:
    if st.sidebar.button("Procesar"):
        st.header("Detección en Tiempo Real Iniciada")

        # Configuración de la cámara
        cap = cv2.VideoCapture(0)  # 0 para cámara interna; cambiar a 1 para cámara externa
        stframe = st.empty()  # Espacio para actualizar los frames

        # Bucle para capturar los fotogramas de la cámara en tiempo real
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("No se pudo obtener la imagen de la cámara.")
                break

            # Preprocesar el fotograma
            img = cv2.resize(frame, (64, 64))  # Ajusta el tamaño a 64x64
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)  # Añadir dimensión extra
            img_array /= 255.0  # Normalizar

            # Realizar la predicción
            predicciones = st.session_state["model"].predict(img_array)
            indice_clase = np.argmax(predicciones)
            porcentaje_prediccion = predicciones[0][indice_clase] * 100
            fruta_predicha = st.session_state["etiquetas_invertidas"][indice_clase]

            # Mostrar el resultado en el fotograma
            texto = f'{fruta_predicha} ({porcentaje_prediccion:.2f}%)'
            cv2.putText(frame, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Convertir de BGR a RGB para mostrar en Streamlit
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame, channels="RGB")

        # Liberar la cámara cuando termine
        cap.release()
else:
    st.warning("Por favor, carga un modelo y etiquetas para empezar la detección.")
