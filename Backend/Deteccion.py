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

model = YOLO("../Backend/Pre-train_model/yolov8s-worldv2-lvis.pt")  # Objetos
model2 = YOLO("../Backend/Pre-train_model/yolo11s.pt")  # Personas

objetos_previos = set()
ultimo_envio = time.time()
ultima_interpretacion = ""  # Almacena la última interpretación generada

class ImageData(BaseModel):
    image: str  # Imagen en base64

def actualizar_interpretacion(objetos_str):
    """Ejecuta el script de Gemini y guarda la respuesta."""
    global ultima_interpretacion
    try:
        resultado = subprocess.run(
            ["python", "./Api-gemini/Interpretacion.py", objetos_str],
            capture_output=True, text=True
        )
        ultima_interpretacion = resultado.stdout.strip()  # Guardar la respuesta
    except Exception as e:
        ultima_interpretacion = f"Error al interpretar la escena: {str(e)}"

@app.post("/predict")
async def predict(image_data: ImageData):
    global objetos_previos, ultimo_envio

    image_bytes = base64.b64decode(image_data.image)
    image_np = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    height, width, _ = frame.shape  
    
    results_objetos = model(frame)
    results_personas = model2(frame)
    
    objetos_detectados = set()
    
    def procesar_resultados(results, modelo):
        nonlocal objetos_detectados
        for result in results:
            if not result.boxes:
                continue
            for box in result.boxes.data:
                x_min, y_min, x_max, y_max, confidence, cls = box.tolist()
                if confidence < 0.40:
                    continue
                
                class_name = modelo.names[int(cls)]
                confidence = float(confidence)
                
                x_center = (x_min + x_max) / 2
                if x_center < width / 3:
                    position = "izquierda"
                elif x_center < 2 * width / 3:
                    position = "centro"
                else:
                    position = "derecha"
                
                objeto_info = f"{class_name} (confianza: {confidence:.2f}, posición: {position})"
                objetos_detectados.add(objeto_info)
    
    procesar_resultados(results_objetos, model)
    procesar_resultados(results_personas, model2)

    print("Objetos detectados:", objetos_detectados)

    if objetos_detectados != objetos_previos and time.time() - ultimo_envio > 3:
        objetos_previos = objetos_detectados
        ultimo_envio = time.time()
        objetos_str = "; ".join(objetos_detectados)

        threading.Thread(target=actualizar_interpretacion, args=(objetos_str,)).start()

    return {"detected_objects": list(objetos_detectados)}

@app.get("/interpretation")
async def get_interpretation():
    """Devuelve la última interpretación generada por Gemini."""
    return {"interpretation": ultima_interpretacion}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)