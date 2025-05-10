import sys
import os
from google import genai
from dotenv import load_dotenv

# Cargar API key
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Crear cliente con la API key
client = genai.Client(api_key=API_KEY)

def interpretar_escena(lista_objetos):
    # Validación: si la lista está vacía o solo contiene espacios
    if not lista_objetos.strip():
        return "No se pudo reconocer el entorno."

    # Instrucción para interpretar la escena
    prompt_instruccion = (
        "Tu tarea es interpretar una escena a partir de una lista de objetos detectados en la imagen, describiendo el entorno de manera clara y comprensible.\n\n"
        "### Reglas para la interpretación:\n"
        "- **Usa solo los objetos con confianza mayor a 0.40** para inferir el tipo de entorno.\n"
        "- **No menciones la lista de objetos directamente**, en su lugar, describe el ambiente que representan.\n"
        "- **Utiliza la información de posición (izquierda, centro, derecha)** para ayudar a contextualizar la escena.\n"
        "- **Si hay objetos relacionados (ejemplo: mesa y silla), interprétalos en conjunto** para dar sentido al espacio.\n"
        "- **Si hay elementos estructurales (puertas, ventanas, escaleras), úsalos para definir el entorno**.\n"
        "- **Evita frases impersonales como 'en la imagen hay...'**, en su lugar, describe el ambiente directamente.\n"
        "-No alargues la respuesta, manténla breve y al grano.\n"
        "- **Si se detectan elementos característicos de un lugar específico (ejemplo: sofá y televisor), asume el tipo de entorno**.\n\n"
        "Si encuentras una lista 'Conifere', 'Feuillu', 'Tree' solo menciona como 'plantas' y no lo interpretes como un objeto específico.\n\n"
        "### Ejemplo:\n"
        "**Entrada:**\n"
        "Cama (confianza: 0.95, coordenadas: [100, 200, 300, 500], posición: centro); "
        "Puerta (confianza: 0.89, coordenadas: [50, 100, 250, 600], posición: derecha); "
        "Lámpara (confianza: 0.92, coordenadas: [200, 50, 280, 150], posición: izquierda)\n\n"
        "**Salida esperada:**\n"
        "Parece que te encuentras en un dormitorio. En el centro se encuentra lo que parece ser una cama, "
        "a la derecha hay una puerta, "
        "y a la izquierda hay una fuente de iluminación, probablemente una lámpara de mesa o de pared. "
        "La combinación de estos elementos indica que es una habitación.\n\n"
        f"Ahora, genera una interpretación detallada del entorno basándote en los objetos detectados con confianza > 0.20:\n{lista_objetos}"
    )

    # Generar respuesta con Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt_instruccion
    )

    return response.text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        objetos_lista = sys.argv[1]
        interpretacion = interpretar_escena(objetos_lista)
        print(interpretacion)
    else:
        # Caso en que no se pasan argumentos
        print("No se pudo reconocer el entorno.")
