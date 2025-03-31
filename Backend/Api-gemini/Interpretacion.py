import sys
import os
from google import genai
from dotenv import load_dotenv

# Cargar API key
load_dotenv()
API_KEY = os.getenv("API_KEY")

client = genai.Client(api_key=API_KEY)

def interpretar_escena(lista_objetos):
    prompt_instruccion = (
        "Necesito que interpretes listas de objetos detectados en una escena y describas el contexto.\n\n"
        "Cada objeto tiene información sobre su confianza y coordenadas en la imagen.\n\n"
        "Ejemplo:\n"
        "Entrada: Cama (confianza: 0.95, coordenadas: [100, 200, 300, 500]); Puerta (confianza: 0.89, coordenadas: [50, 100, 250, 600])\n"
        "Salida esperada: Parece que estás en un dormitorio con una cama grande y una puerta al fondo.\n\n"
        "Reglas:\n"
        "- No uses frases como 'parece que estás describiendo'.\n"
        "- La descripción debe ser clara para una persona con discapacidad visual.\n"
        "- No uses palabras como 'puede ser' o 'quizás'.\n"
        "- Considera la posición de los objetos en la imagen.\n"
        "- Si hay un objeto grande y centrado, puede ser el foco de la escena.\n\n"
        f"Ahora, dame la interpretación de la siguiente lista de objetos:\n{lista_objetos}"
    )

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
        print("Error: No se recibió una lista de objetos como argumento.")
