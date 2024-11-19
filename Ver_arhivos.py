import os
import re
from collections import Counter

# Directorio donde están tus imágenes
ruta_imagenes = 'C:\\Users\\joelm\\Desktop\\Newfolder\\fruit-recognition-DatasetNinja\\ds\\img'
  

# Lista para almacenar todas las palabras detectadas en los nombres de los archivos
nombres_detectados = []

# Procesa cada archivo en la carpeta
for archivo in os.listdir(ruta_imagenes):
    # Asegúrate de que es una imagen
    if archivo.endswith(('.jpg', '.jpeg', '.png')):  # Añade otros formatos si es necesario
        # Divide el nombre en palabras usando una expresión regular para separar números y letras
        palabras = re.findall(r'[A-Za-z]+', archivo)
        nombres_detectados.extend(palabras)

# Contar las ocurrencias de cada palabra
contador_nombres = Counter(nombres_detectados)

# Mostrar las palabras más comunes, revisa si alguna es una fruta
print("Posibles nombres de frutas en los archivos:")
for palabra, frecuencia in contador_nombres.most_common(20):  # Ajusta el número según necesites
    print(f"{palabra}: {frecuencia}")
