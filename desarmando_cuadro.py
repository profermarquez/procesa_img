import cv2
import os
from tkinter import Tk, filedialog

# Abrir una ventana para seleccionar una imagen
def seleccionar_imagen():
    Tk().withdraw()  # Ocultar la ventana principal de Tkinter
    ruta_imagen = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Archivos de imagen", "*.jpg;*.png")])
    return ruta_imagen

# Seleccionar la imagen
image_path = seleccionar_imagen()
if not image_path:
    print("No se seleccionó ninguna imagen. Saliendo...")
    exit()

# Cargar la imagen
image = cv2.imread(image_path)
if image is None:
    print(f"Error al cargar la imagen en la ruta: {image_path}")
    exit()

# Mostrar la imagen cargada
cv2.imshow("Imagen Cargada", image)
cv2.waitKey(2000)
cv2.destroyAllWindows()

base_name = os.path.splitext(os.path.basename(image_path))[0]


import cv2
import os
import numpy as np
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from PIL import Image

# Deshabilitar advertencias de torch.meshgrid
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="torch.meshgrid")

# Configurar Detectron2 para segmentación de personas
cfg = get_cfg()
cfg.MODEL.DEVICE = "cpu" ##cfg.MODEL.DEVICE = "cuda"
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

predictor = DefaultPredictor(cfg)
outputs = predictor(image)

# Extraer máscaras y categorías
masks = outputs["instances"].pred_masks.to("cpu").numpy()
classes = outputs["instances"].pred_classes.to("cpu").numpy()

# Directorio para guardar los recortes
output_dir = "./recortes"
os.makedirs(output_dir, exist_ok=True)

# Guardar cada objeto detectado de clase 'persona'
for i, mask in enumerate(masks):
    if classes[i] == 0:  # '0' representa la clase 'persona' en COCO
        mask = mask.astype(np.uint8) * 255

        # Crear una imagen RGBA con el canal alfa basado en la máscara
        rgba_image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        rgba_image[:, :, 3] = mask

        # Recortar el área del objeto
        x, y, w, h = cv2.boundingRect(mask)
        cropped_object = rgba_image[y:y + h, x:x + w]

        # Guardar el recorte con fondo transparente
        output_path = os.path.join(output_dir, f"{base_name}_recorte_{i}.png")
        Image.fromarray(cropped_object).save(output_path)
        print(f"Recorte guardado en: {output_path}")

# Mostrar el número total de recortes
print(f"Se guardaron {len(masks)} recortes de personas en '{output_dir}'")
