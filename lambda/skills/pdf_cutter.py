import PyPDF2
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


# 0     1  2   3   4  5  6 7
# corta el pdf $id de p1 a 20
def main(params: tuple):
  # catch the params
  message, member, server = params
  # split the message
  splited_message = message.split(' ')
  # first get the id
  file_id = splited_message[3][1:]
  # second the pages
  page_from, page_to = int(splited_message[5]), int(splited_message[7])
  # get the file path
  file_path = f'lambdrive/documents/{file_id}.pdf'
  # generate a new hash
  new_hash = generate_hash(f"{file_id}_{splited_message[5]}_{splited_message[7]}")
  # and the detination file_path
  file_destination = f'lambdrive/documents/{new_hash}.pdf'
  # call the function
  extraer_paginas(file_path, page_from, page_to, file_destination)
  return [
    {
      "type": "text",
      "content": f"Listo, tu PDF de la página {page_from} a la {page_to} está disponible como:```${new_hash}```"
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
> **Comando:** Lambda corta el pdf de **página** a **página**
> **Ejemplo 1:** Lambda corta el pdf $123ab de 10 a 20
> **Ejemplo 2:** Lambda corta el pdf $123ab desde 100 a 200
"""