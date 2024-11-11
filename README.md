# Detección de Frutas en Tiempo Real

Esta aplicación permite realizar la detección de frutas en tiempo real utilizando un modelo de clasificación preentrenado en formato `.h5` y un archivo de etiquetas en formato `.npy`. La aplicación, desarrollada con Streamlit y OpenCV, utiliza la cámara del usuario para capturar video y mostrar el nombre de la fruta detectada junto con el porcentaje de certeza.

## Características

- **Carga de Modelo y Etiquetas**: El usuario puede cargar su propio modelo `.h5` y un archivo de etiquetas `.npy`.
- **Detección en Tiempo Real**: Accede a la cámara del usuario y realiza la detección de frutas en tiempo real.
- **Interfaz Intuitiva**: La aplicación utiliza Streamlit para ofrecer una interfaz amigable y de fácil uso.

## Requisitos

- Python 3.7 o superior
- Modelo de clasificación de frutas en formato `.h5`
- Archivo de etiquetas de clase en formato `.npy`

## Instalación

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias utilizando el archivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

   El archivo `requirements.txt` debe contener las siguientes bibliotecas:

    ```plaintext
    streamlit
    tensorflow
    opencv-python-headless
    Pillow
    ```

## Ejecución de la Aplicación

1. Para iniciar la aplicación, ejecuta el siguiente comando en tu terminal:

    ```bash
    streamlit run app.py
    ```

2. Abre tu navegador y dirígete a `http://localhost:8501` para ver la aplicación en funcionamiento.

## Uso de la Aplicación

### Cargar el Modelo y las Etiquetas

1. En la barra lateral de la aplicación, haz clic en **"Paso 1: Cargar el Modelo"** y selecciona tu archivo `.h5` de modelo de frutas.
2. Luego, en **"Paso 2: Cargar las Etiquetas de Clase"**, selecciona el archivo `.npy` que contiene las etiquetas de clase.

### Iniciar la Detección en Tiempo Real

Una vez que el modelo y las etiquetas estén cargados correctamente:
1. Haz clic en el botón **"Procesar"** en la barra lateral para activar la cámara.
2. La aplicación mostrará el video en tiempo real y, para cada cuadro, el nombre de la fruta detectada y el porcentaje de certeza.

## Despliegue en Streamlit Cloud

# Para desplegar la aplicación en Streamlit Cloud:

1. **Sube el Proyecto a un Repositorio de GitHub**: Asegúrate de incluir `app.py`, `requirements.txt`, y cualquier archivo de prueba.

2. **Configura el Despliegue**:
   - En [Streamlit Cloud](https://streamlit.io/cloud), crea una nueva aplicación.
   - Selecciona el repositorio de GitHub y elige el archivo `app.py` como archivo de inicio.

3. **Inicia el Despliegue**: Haz clic en **Deploy** para iniciar la aplicación en la nube.

## Notas Adicionales

- **Compatibilidad del Navegador**: Asegúrate de que el navegador permita el acceso a la cámara. Algunos navegadores pueden solicitar permiso para acceder a la cámara.
- **Requisitos de Memoria**: La aplicación utiliza TensorFlow, por lo que puede requerir una cantidad significativa de memoria, especialmente en la nube.



Este `README.md` está estructurado para brindar una guía completa sobre la instalación, configuración, ejecución y despliegue de tu aplicación en Streamlit.
