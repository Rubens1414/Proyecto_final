from fastapi import FastAPI
import cv2
import numpy as np
import base64
import subprocess
import threading
from ultralytics import YOLO, YOLOWorld
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Carga los modelos una sola vez al iniciar
model_objects = YOLOWorld("../Backend/Pre-train_model/Yolo_world_LVIS.pt")  
model_persons = YOLO("../Backend/Pre-train_model/yolo11s.pt")    
model_trees = YOLO("../Backend/Pre-train_model/yolo11n_tree.pt")           

# Variables globales
ultima_interpretacion = ""          

class ImageData(BaseModel):
    image: str
#Función para actualizar la interpretación de la escena
def actualizar_interpretacion(objetos_str: str):
    """Llama al script externo para interpretar la lista de objetos detectados."""
    global ultima_interpretacion
    try:
        resultado = subprocess.run(
            ["python", "./Api-gemini/Interpretacion.py", objetos_str],
            capture_output=True, text=True
        )
        print('resultado', resultado)
        ultima_interpretacion = resultado.stdout.strip()
    except Exception as e:
        ultima_interpretacion = f"Error al interpretar la escena: {str(e)}"

# Calcular la posición del objeto en la imagen
def calcular_posicion(x_center, y_center, width, height):
    if y_center < height / 3:
        vertical = "arriba"
    elif y_center < 2 * height / 3:
        vertical = "centro"
    else:
        vertical = "abajo"

    if x_center < width / 3:
        horizontal = "izquierda"
    elif x_center < 2 * width / 3:
        horizontal = "centro"
    else:
        horizontal = "derecha"

    return f"{vertical} {horizontal}"

# Endpoint para recibir la imagen y devolver los objetos detectados
@app.post("/predict")
async def predict(image_data: ImageData):
    global ultima_interpretacion
    image_bytes = base64.b64decode(image_data.image)
    image_np = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    height, width, _ = frame.shape

    # Corre detección con todos los modelos
    results_objetos = model_objects.predict(frame, conf=0.3, verbose=False)
    results_personas = model_persons.predict(frame, conf=0.3, verbose=False)
    results_trees = model_trees.predict(frame, conf=0.3, verbose=False)

    objetos_detectados = set()

    # Procesador general con filtro por nombre de clase (opcional)
    def procesar_resultados(results, modelo, incluir_clases=None, excluir_clases=None):
        for result in results:
            if result.boxes is None:
                continue
            for box in result.boxes.data:
                x_min, y_min, x_max, y_max, confidence, cls = box.tolist()

                if confidence < 0.4:
                    continue

                class_id = int(cls)
                class_name = modelo.names.get(class_id, f"Clase_{class_id}")

                if incluir_clases and class_name not in incluir_clases:
                    continue
                if excluir_clases and class_name in excluir_clases:
                    continue

                objeto_width = x_max - x_min
                objeto_height = y_max - y_min
                x_center = x_min + objeto_width / 2
                y_center = y_min + objeto_height / 2

                position = calcular_posicion(x_center, y_center, width, height)

                objeto_info = f"{class_name} (confianza: {confidence:.2f}, posición: {position})"
                objetos_detectados.add(objeto_info)

    # Procesa detecciones
    procesar_resultados(results_objetos, model_objects, excluir_clases=["person"])
    procesar_resultados(results_personas, model_persons, incluir_clases=["person"])
    procesar_resultados(results_trees, model_trees)  

    print("Objetos detectados:", objetos_detectados)

    objetos_str = "; ".join(objetos_detectados)
    actualizar_interpretacion(objetos_str)  
    return {"detected_objects": list(objetos_detectados)}

@app.get("/interpretation")
async def get_interpretation():
    return {"interpretation": ultima_interpretacion}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
