import sys
import base64
import pyperclip
import os

# Verificar si se proporcionó el nombre del archivo como argumento al ejecutar el script
if len(sys.argv) < 2:
    print("Error: Debes proporcionar el nombre del archivo como argumento al ejecutar el script.")
else:
    file_name = "sample-files/" + sys.argv[1]

    # Verificar si el archivo existe
    if os.path.exists(file_name):
        with open(file_name, "rb") as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content).decode('utf-8')
            pyperclip.copy(encoded_content)
            print("El contenido del archivo ha sido codificado en base64 y copiado al portapapeles.")
    else:
        print("Error: El archivo especificado no se encontró.")