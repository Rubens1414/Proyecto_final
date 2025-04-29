from fastapi import FastAPI
import cv2
import numpy as np
import base64
import time
import subprocess
import threading
from ultralytics import YOLO
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Carga los modelos una sola vez al iniciar
model_objects = YOLO("../Backend/Pre-train_model/yolov8s-worldv2-lvis.pt")  
model_persons = YOLO("../Backend/Pre-train_model/yolo11s.pt")               

# Variables globales
ultima_interpretacion = ""          # Última interpretación generada

# Clase que define el formato del POST
class ImageData(BaseModel):
    image: str

def actualizar_interpretacion(objetos_str: str):
    """Llama al script externo para interpretar la lista de objetos detectados."""
    global ultima_interpretacion
    try:
        resultado = subprocess.run(
            ["python", "./Api-gemini/Interpretacion.py", objetos_str],
            capture_output=True, text=True
        )
        ultima_interpretacion = resultado.stdout.strip()
    except Exception as e:
        ultima_interpretacion = f"Error al interpretar la escena: {str(e)}"

def calcular_posicion(x_center, y_center, width, height):
    """Calcula una mejor posición del objeto (no solo en X sino también en Y)."""
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

@app.post("/predict")
async def predict(image_data: ImageData):
    global ultima_interpretacion
    image_bytes = base64.b64decode(image_data.image)
    image_np = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    height, width, _ = frame.shape

    # Corre detección con ambos modelos
    results_objetos = model_objects.predict(frame, conf=0.4, verbose=False)
    results_personas = model_persons.predict(frame, conf=0.4, verbose=False)

    objetos_detectados = set()

    # Función para procesar resultados de detección
    def procesar_resultados(results, modelo):
        for result in results:
            if result.boxes is None:
                continue
            for box in result.boxes.data:
                x_min, y_min, x_max, y_max, confidence, cls = box.tolist()

                if confidence < 0.4:
                    continue

                class_name = modelo.names.get(int(cls), f"Clase_{int(cls)}")
                confidence = float(confidence)

                objeto_width = x_max - x_min
                objeto_height = y_max - y_min
                x_center = x_min + objeto_width / 2
                y_center = y_min + objeto_height / 2

                # Calcula posición avanzada
                position = calcular_posicion(x_center, y_center, width, height)

                # Arma la descripción del objeto
                objeto_info = f"{class_name} (confianza: {confidence:.2f}, posición: {position})"
                objetos_detectados.add(objeto_info)

    # Procesa detecciones de ambos modelos
    procesar_resultados(results_objetos, model_objects)
    procesar_resultados(results_personas, model_persons)

    print("Objetos detectados:", objetos_detectados)

    # Siempre interpreta (no importa si la imagen es la misma o no)
    objetos_str = "; ".join(objetos_detectados)
    threading.Thread(target=actualizar_interpretacion, args=(objetos_str,)).start()

    return {"detected_objects": list(objetos_detectados)}

@app.get("/interpretation")
async def get_interpretation():
    return {"interpretation": ultima_interpretacion}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)