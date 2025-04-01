

## 1. Instalación y Ejecución del Servidor

### Requisitos Previos
- fastapi
- opencv-python
- numpy
- uvicorn
- ultralytics
- pydantic
- google-generativeai
- python-dotenv
- Un archivo `.env` con la variable `API_KEY` de Gemini se debe ubicar en ./Backend

### Instalar las dependecias en el Backend
Ejecuta los siguientes comandos en la terminal:
```bash
pip install -r requirements.txt
```

### Ejecutar el Servidor FastAPI 
```bash
uvicorn Deteccion:app --host 0.0.0.0 --port 8000
```
Por defecto, el servidor corre en `http://0.0.0.0:8000`.

---

##  2. Conexión entre Flutter y el Servidor

###  Flujo de Datos
1. **Flutter** captura una imagen y la convierte en base64.
2. **Se envía la imagen al endpoint** `http://0.0.0.0:8000/predict`.
3. **FastAPI procesa la imagen** con YOLO y extrae los objetos detectados con coordenadas (Se debe mejorar para que sea mas preciso).
4. **Si hay cambios en la detección**, los envía a `Interpretacion.py` para obtener la descripción de la escena.
5. **Gemini genera la interpretación** Pero solo lo muestra en la consola de python.

## 3. Iniciar Flutter y Configurar el Emulador

### Requisitos Previos
- Tener instalado [Flutter](https://flutter.dev/docs/get-started/install) en tu sistema.
- Instalar Android Studio y configurar un emulador de Android.

### Pasos para Ejecutar la Aplicación Flutter
1. Asegúrate de que tienes Flutter correctamente instalado ejecutando:
   ```bash
   flutter doctor
   ```
2. Abre Android Studio y configura un emulador Android.
3. Abre el proyecto Flutter en tu editor de preferencia (Android Studio o VS Code).
4. Con el emulador corriendo, ejecuta la aplicación con:
   ```bash
   flutter run
   ```

### Funcionamiento de la Aplicación por ahora
- La aplicación abre la cámara.
- Cuando el usuario toma una foto al undirle a la camara, la imagen se convierte en base64 y se envía al servidor FastAPI.
- El servidor responde con los objetos detectados (por mejorar la precisión).
- Actualmente, la interpretación de la escena solo se muestra en la consola de Python.




