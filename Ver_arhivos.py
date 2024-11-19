import os
import re
from collections import Counter

# Directorio donde están tus imágenes(cambiar si es necesario)
ruta_imagenes = 'C:\\Users\\joelm\\Desktop\\Newfolder\\fruit-recognition-DatasetNinja\\ds\\img'
  

# Lista para almacenar todas las palabras detectadas en los nombres de los archivos
nombres_detectados = []

# Procesa cada archivo en la carpeta
for archivo in os.listdir(ruta_imagenes):
    # Ver si es una imagen
    if archivo.endswith(('.jpg', '.jpeg', '.png')):  # Añade otros formatos si es necesario
        palabras = re.findall(r'[A-Za-z]+', archivo)
        nombres_detectados.extend(palabras)

# Contar las ocurrencias de cada palabra
contador_nombres = Counter(nombres_detectados)

# Mostrar las palabras más comunes y revisar si alguna es una fruta
print("Posibles nombres de frutas en los archivos:")
for palabra, frecuencia in contador_nombres.most_common(20):  # Ajusta el número 
    print(f"{palabra}: {frecuencia}")
