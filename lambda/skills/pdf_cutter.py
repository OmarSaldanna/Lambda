import json
import PyPDF2
import requests
from core.modules import generate_hash

def extraer_paginas(pdf_path, start_page, end_page, output_path):
  with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    writer = PyPDF2.PdfWriter()

    for page_number in range(start_page - 1, end_page):
      page = reader.pages[page_number]
      writer.add_page(page)

    with open(output_path, 'wb') as output_pdf:
      writer.write(output_pdf)

def get_user_file(user_id):
  return user_data = requests.get('http://127.0.0.1:8081/members', json={
    "db": "members",
    "id": user_id
  })['answer']['file']

def set_user_file(user_id, file_hash):
  requests.put('http://127.0.0.1:8081/members', json={
    "db": "members",
    "id": user_id,
    "data": json.dumps({
      "file": file_hash
    })
  })

# 0     1  2   3  4  5 6 
# corta el pdf de p1 a p2
# extrae del pdf de p1 a p2
# recorta del pdf de p1 a p2
def main(params: tuple):
  # catch the params
  message, member, server = params
  # split the message
  splited_message = message.split(' ')
  # first get the id
  file_id = get_user_file(member)
  # second the pages
  page_from, page_to = int(splited_message[4]), int(splited_message[6])
  # get the file path
  file_path = f'lambdrive/documents/{file_id}.pdf'
  # generate a new hash
  new_hash = generate_hash(f"{file_id}_{splited_message[4]}_{splited_message[6]}")
  # and the detination file_path
  file_destination = f'lambdrive/documents/{new_hash}.pdf'
  # try to call the function
  try:
    extraer_paginas(file_path, page_from, page_to, file_destination)
  # if there was an error then return it
  except:
    return [{
      "type": "error", "content": f"Lo siento <@{member}> no encontramos tu archivo, **subirlo de nuevo podría resolver esto.**"
    }]
  # finally the file was saved
  # then save the new hash in the user db
  set_user_file(member, new_hash)
  # and return the file
  return [
    {
      "type": "text",
      "content": f"Listo, tu PDF de la página {page_from} a la {page_to} está disponible para usarse."
    },
    {
      "type": "file",
      "content": file_destination
    }
  ]

# info about the skill
info = """
### PDF Cutter
Esta función permite cortar PDFs, solo dile entre que páginas cortar y **Lambda te dará el archivo cortado y su id para que lo puedas usar con la función de leer PDFs de Lambda**.
> **Comando:** Lambda [corta, recorta o extrae] el [pdf o archivo] de [id del pdf] de **página** a **página**
> **Ejemplo 1:** Lambda corta el pdf de $123ab de 10 a 20
> **Ejemplo 2:** Lambda recorta del pdf de $123ab desde 100 a 200
> **Ejemplo 3:** Lambda extrae las paginas de $123ab desde 100 a 200
"""