import os
from PIL import Image

# Ruta a la carpeta principal donde están organizadas las imágenes por frutas
ruta_carpeta = 'C:\\Users\\joelm\\Desktop\\Newfolder\\data_organizada'  # Reemplaza con la ruta de tu carpeta principal de imágenes

# Tamaño deseado
nuevo_tamano = (128, 128)

# Recorre cada subcarpeta y redimensiona las imágenes
for carpeta_fruta in os.listdir(ruta_carpeta):
    ruta_fruta = os.path.join(ruta_carpeta, carpeta_fruta)
    
    # Verifica que sea una carpeta
    if os.path.isdir(ruta_fruta):
        for archivo in os.listdir(ruta_fruta):
            ruta_imagen = os.path.join(ruta_fruta, archivo)
            
            # Verifica que es un archivo de imagen
            if archivo.endswith(('.jpg', '.jpeg', '.png')):  # Añade más formatos si es necesario
                with Image.open(ruta_imagen) as img:
                    # Redimensiona la imagen
                    img_resized = img.resize(nuevo_tamano)
                    
                    # Guarda la imagen redimensionada, reemplazando la original
                    img_resized.save(ruta_imagen)
                    print(f"Redimensionado: {ruta_imagen}")

