import os
from rembg import remove
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# 📂 Crear directorios para almacenar las imágenes
os.makedirs('original', exist_ok=True)
os.makedirs('masked', exist_ok=True)

# 🖼️ Seleccionar la imagen principal (la que tendrá el fondo eliminado)
def seleccionar_imagen():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    file_path = filedialog.askopenfilename(title="Selecciona una imagen para quitar el fondo",
                                           filetypes=[("Imágenes", "*.jpg;*.jpeg;*.png")])
    return file_path

# Seleccionar la imagen
img_path = seleccionar_imagen()
if not img_path:
    print("No se seleccionó ninguna imagen. Saliendo...")
    exit()

# Extraer el nombre del archivo
img_name = os.path.basename(img_path)

# Copiar la imagen seleccionada al directorio 'original'
try:
    img = Image.open(img_path)
    img.save(f'original/{img_name}', format='JPEG')
    print(f"Imagen '{img_name}' guardada en 'original/' correctamente.")
except Exception as e:
    print(f"Error al guardar la imagen: {e}")
    exit()

# 🌌 Quitar el fondo de la imagen seleccionada
output_path = f'masked/{img_name}'
try:
    with open(output_path, 'wb') as f:
        input_image = open(f'original/{img_name}', 'rb').read()
        result = remove(input_image, alpha_matting=True)
        f.write(result)
    print(f"Imagen sin fondo guardada en: {output_path}")
except Exception as e:
    print(f"Error al eliminar el fondo de la imagen: {e}")
    exit()

# 🖼️ Seleccionar una imagen de fondo
def seleccionar_fondo():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Selecciona una imagen de fondo",
                                           filetypes=[("Imágenes", "*.jpg;*.jpeg;*.png")])
    return file_path

# Seleccionar imagen de fondo
bk_img_path = seleccionar_fondo()
if not bk_img_path:
    print("No se seleccionó ninguna imagen de fondo. Saliendo...")
    exit()

try:
    # Cargar las imágenes
    background = Image.open(bk_img_path)
    foreground = Image.open(output_path)

    # Redimensionar el fondo al tamaño de la imagen del primer plano
    background = background.resize(foreground.size)

    # Pegar la imagen sin fondo sobre el fondo seleccionado
    background.paste(foreground, (0, 0), foreground)
    
    # Guardar la imagen final
    final_path = 'original/background_combined.jpg'
    background.save(final_path, format='JPEG')

    print(f"Imagen combinada guardada en: {final_path}")

except Exception as e:
    print(f"Error al combinar imágenes: {e}")
    exit()

# Mostrar la imagen final
background.show()
