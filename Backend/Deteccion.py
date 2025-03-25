from PIL import Image
from ultralytics import YOLO  
import os
import subprocess  

# Obtener la ruta del script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Cargar el modelo YOLO
modelo_path = os.path.join(base_dir, "Pre-train_model", "yolo11n.pt")
model = YOLO(modelo_path)

def detectar_objetos(imagen_path):
    """
    Detecta objetos en una imagen y devuelve una lista con sus nombres.
    """
    image = Image.open(imagen_path)
    results = model(image)

    objetos_detectados = []  

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0].item()) 
            class_name = model.names[cls] 

            if class_name not in objetos_detectados: 
                objetos_detectados.append(class_name)

    return objetos_detectados

imagen_prueba = os.path.join(base_dir, "Images", "cocina_p.jpg")

if os.path.exists(imagen_prueba):
    print(f"Imagen encontrada: {imagen_prueba}")

    # Obtener la lista de objetos detectados
    objetos = detectar_objetos(imagen_prueba)
    print(f"🔹 Objetos detectados: {objetos}")

   
    objetos_str = ",".join(objetos)

    subprocess.run(["python", os.path.join(base_dir, "Api-gemini", "interpretacion.py"), objetos_str])

else:
    print(f"La imagen no se encuentra en {imagen_prueba}")
