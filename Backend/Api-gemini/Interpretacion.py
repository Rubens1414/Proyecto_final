import sys
import os
from google import genai
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

API_KEY = os.getenv("API_KEY")

client = genai.Client(api_key=API_KEY)

def interpretar_escena(lista_objetos):
    objetos_str = ", ".join(lista_objetos)

    prompt_instruccion = (
        "Necesito que interpretes listas de objetos y describas el contexto en el que suelen encontrarse.\n\n"
        "Ejemplo:\n"
        "Entrada: Cama, puerta, vaso, abanico\n"
        "Salida esperada: Estas en un cuerto en el que tiene una cama cerca una puerta .\n\n"
        "Formato de salida requerido:\n"
        "- No uses frases como 'parece que estás describiendo'.\n"
        "- Ten en cuenta que es para personas con discapacidad visual asi que se claro.\n\n"
        "- No digas observas, miras, ves, etc.\n"
        "- Intenta adivinar el contexto en el que se encuentran los objetos.\n"
        f"Ahora, dame la interpretación de la siguiente lista de objetos:\n{objetos_str}"
    )

    # Enviar solicitud a Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt_instruccion
    )

    # Retornar la respuesta del modelo
    return response.text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        objetos_lista = sys.argv[1].split(",")  # Convertir string en lista
        interpretacion = interpretar_escena(objetos_lista)
        print(interpretacion)
    else:
        print(" Error: No se recibió una lista de objetos como argumento.")
