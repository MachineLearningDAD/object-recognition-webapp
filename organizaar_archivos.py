import os
import shutil

# Directorio donde están todas las imagenes
ruta_imagenes = 'C:\\Users\\joelm\\Desktop\\Newfolder\\fruit-recognition-DatasetNinja\\ds\\img'  # Reemplaza con la ruta de tu carpeta de imagenes

# Directorio donde vanlas imagenes para organizar 
ruta_destino = 'C:\\Users\\joelm\\Desktop\\Newfolder\\data_organizada'  # Reemplaza con la ruta donde quieres organizar las imagenes

# Asegúrate de que el directorio de destino exista
if not os.path.exists(ruta_destino):
    os.makedirs(ruta_destino)

# Lista todos los archivos en el directorio de imagenes
for archivo in os.listdir(ruta_imagenes):
    if archivo.endswith(('.jpg', '.jpeg', '.png')):  # Añade otros formatos si es necesario
        # Extraer el nombre de la fruta del nombre del archivo
        nombre_fruta = ''
        if 'banana' in archivo.lower():
            nombre_fruta = 'banana'
        elif 'apple' in archivo.lower():
            nombre_fruta = 'apple'
        elif 'orange' in archivo.lower():
            nombre_fruta = 'orange'
        elif 'kiwi' in archivo.lower():
            nombre_fruta = 'kiwi'
        elif 'mango' in archivo.lower():
            nombre_fruta = 'mango'
        elif 'peach' in archivo.lower():
            nombre_fruta = 'peach'
        elif 'pitaya' in archivo.lower():
            nombre_fruta = 'pitaya'
        elif 'tomatoes' in archivo.lower():
            nombre_fruta = 'tomatoes'
        elif 'carambola' in archivo.lower():
            nombre_fruta = 'carambola'
        # Agrega más elif para otras frutas si es necesario

        # Si se detecto una fruta, mueve el archivo a la carpeta donde va
        if nombre_fruta:
            ruta_fruta = os.path.join(ruta_destino, nombre_fruta)
            if not os.path.exists(ruta_fruta):
                os.makedirs(ruta_fruta)
            
            # Mueve el archivo a la carpeta de la fruta
            shutil.move(os.path.join(ruta_imagenes, archivo), os.path.join(ruta_fruta, archivo))
            print(f'Moviendo {archivo} a {ruta_fruta}')
