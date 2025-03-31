from fastapi import FastAPI
import cv2
import numpy as np
import base64
import time
import subprocess
from ultralytics import YOLO
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Cargar modelo YOLO
model = YOLO("../Backend/Pre-train_model/yolo11n.pt")
objetos_previos = set()
ultimo_envio = time.time()

class ImageData(BaseModel):
    image: str  # Imagen en base64

@app.post("/predict")
async def predict(image_data: ImageData):
    global objetos_previos, ultimo_envio

    # Decodificar la imagen
    image_bytes = base64.b64decode(image_data.image)
    image_np = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    results = model(frame)
    objetos_detectados = []

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0].item())
            class_name = model.names[cls]
            confidence = box.conf.item()
            x_min, y_min, x_max, y_max = map(int, box.xyxy[0].tolist())

            objetos_detectados.append(
                f"{class_name} (confianza: {confidence:.2f}, "
                f"coordenadas: [{x_min}, {y_min}, {x_max}, {y_max}])"
            )

    # Enviar solo si hay cambios y ha pasado suficiente tiempo
    if set(objetos_detectados) != objetos_previos and time.time() - ultimo_envio > 3:
        objetos_previos = set(objetos_detectados)
        ultimo_envio = time.time()
        objetos_str = "; ".join(objetos_detectados)
        subprocess.Popen(["python", "./Api-gemini/Interpretacion.py", objetos_str])

    return {"detected_objects": objetos_detectados}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
