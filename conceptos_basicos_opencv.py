import cv2
import numpy as np
from matplotlib import pyplot as plt

# Configurar el tamaño de las imágenes a mostrar
plt.rcParams['figure.figsize'] = (10, 8)

# Ruta de la imagen cargada
image_path = "gato.jpg"

# Cargar la imagen
input_image = cv2.imread(image_path)

if input_image is None:
    print(f"Error al cargar la imagen en la ruta: {image_path}")
    exit()

# Mostrar información básica de la imagen
print(f"Tamaño de la imagen: {input_image.size} píxeles")
print(f"Dimensiones (Alto, Ancho, Canales): {input_image.shape}")
print(f"Tipo de dato: {input_image.dtype}")

# Mostrar la imagen cargada en RGB
opencv_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
plt.imshow(opencv_image)
plt.title("Imagen Original: Gatos Sospechosos")
plt.show()


# 🎨 **Separar y mostrar canales RGB**
b, g, r = cv2.split(input_image)

# Mostrar el canal rojo
plt.imshow(r, cmap='gray')
plt.title("Canal Rojo - Detectando el Calor de la Mirada del Gato Negro")
plt.show()


# 🔀 **Fusión de canales**
merged_image = cv2.merge([r, g, b])  # Fusionar los canales en el orden RGB
plt.imshow(merged_image)
plt.title("Imagen Fusionada en RGB: Los Gatos Unidos")
plt.show()


# 🎨 **Conversión a otros espacios de color**
hsv_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
plt.imshow(hsv_image[:, :, 1], cmap='gray')
plt.title("Canal de Saturación (HSV) - Intensidad de la Mirada Felina")
plt.show()


# 🔍 **Manipulación de píxeles individuales**
pixel = input_image[100, 100]
print(f"Valor del píxel en (100, 100) antes: {pixel}")

# Cambiar el valor del píxel
input_image[100, 100] = [0, 0, 0]
nuevo_pixel = input_image[100, 100]
print(f"Valor del píxel en (100, 100) después: {nuevo_pixel}")

# Mostrar la imagen con el cambio
plt.imshow(cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB))
plt.title("Imagen con un Píxel Cambiado - Ojos Más Sospechosos")
plt.show()


# 🐱 **Recortar una región específica (cara del gato negro)**
catface = input_image[60:250, 70:350]
plt.imshow(cv2.cvtColor(catface, cv2.COLOR_BGR2RGB))
plt.title("Recorte de la Cara del Gato Negro Sospechoso")
plt.show()


# 🖼️ **Ajustar el tamaño del recorte si es necesario**
fresh_image = cv2.imread(image_path)

# Calcular el tamaño disponible en la imagen destino
y_start, x_start = 200, 200
y_end = y_start + catface.shape[0]
x_end = x_start + catface.shape[1]

# Verificar límites de la imagen
height, width, _ = fresh_image.shape

# Ajustar si excede los límites
y_end = min(y_end, height)
x_end = min(x_end, width)

# Ajustar el recorte si es necesario
adjusted_catface = catface[:y_end - y_start, :x_end - x_start]

# Insertar el recorte en la imagen
fresh_image[y_start:y_end, x_start:x_end] = adjusted_catface

plt.imshow(cv2.cvtColor(fresh_image, cv2.COLOR_BGR2RGB))
plt.title("Imagen con Cara del Gato Negro Insertada")
plt.show()


# ✂️ **Recorte y manipulación con NumPy**
crop = fresh_image[100:400, 130:300]
plt.imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
plt.title("Recorte de una Región Aleatoria de la Imagen")
plt.show()


# 🎯 **Recorte en espacio HSV (canal de saturación)**
hsv_crop = hsv_image[100:400, 100:300, 1]
plt.imshow(hsv_crop, cmap="gray")
plt.title("Recorte del Canal de Saturación (HSV) - Intensidad Felina")
plt.show()


# 🔍 **Explorando las constantes de conversión de color**
color_flags = [flag for flag in dir(cv2) if flag.startswith('COLOR')]
print(f"Total de banderas de color disponibles en OpenCV: {len(color_flags)}")
