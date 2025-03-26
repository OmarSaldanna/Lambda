import os
# module to read pdfs
import PyPDF2
# module to use LLMs
from core.ai import AI
# function to count tokens
from modules.context import string_tokens


def get_text_from_pdf(pdf_path: str):
  # create the PdfReader object
  pdf_file = PyPDF2.PdfReader(open(pdf_path, "rb"))
  # start saving the text
  text = """"""
  # for each page of the pdf
  for page_num in range(len(pdf_file.pages)):
    # get the text of the page
    page_content = pdf_file.pages[page_num].extract_text()
    # add the page to the result
    text += page_content
  # replace \n for spaces and strip
  text = text.replace('\n', ' ').strip()
  return text


# 0   1  2   3 4
# lee el pdf y ...
# lee el pdf y ...
# mira el documento y ...
# ve el documento y ...
# revisa el documento y ...
def main(params: tuple):
  # catch the params
  message, member, server = params
  # instance the AI
  ai = ai(member, server, db=db) # use the db from error
  # get the file id
  file_id = ai.user_data['file']
  # get the file path
  file_path = f'lambdrive/{member}/documents/{file_id}.pdf'

################# Read the file ##########################################

  # try extract the text
  try:
    # pdf_text += get_text_from_pdf(file_path)
    prompt = f"""Eres un asistente inteligente diseñado para proporcionar respuestas precisas basadas en el contenido del archivo PDF que se te proporciona. Por favor, responde a las siguientes consultas según el texto contenido en el archivo PDF. Si no puedes encontrar información relevante en el PDF, responde con "Lo siento, no pude encontrar información relevante". Aquí tienes el contenido del archivo PDF:

{get_text_from_pdf(file_path)}

Por favor, responde las las siguientes preguntas sobre el contenido del archivo:"""
  
  # it there where an error on the file
  except Exception as e:
    # send an error message
    return [{
      "type": "error",
      "content": f"Lo siento <@{member}>, no encontramos tu archivo, subirlo de nuevo podría resolver esto."
    }]

################ Check the tokens ########################################

  if string_tokens(prompt) > int(os.environ["MAX_LARGE_TOKENS"]):
    return [{
      "type": "error",
      "content": f"Lo siento <@{member}>, tu archivo es demasiado extenso, prueba extraer solo las páginas que necesites: [SEPARAR PDF](https://www.ilovepdf.com/split_pdf)"
    }]

################ And anser #############################################

  # get the question
  question = ' '.join(message.split(' ')[4:])
  # add it to promt
  prompt += question
  # and use the AI
  return ai(question, "large")




# info about the skill
info = """
Lector de PDFs
Esta función permite que Lambda lea un archivo PDF de aproximadamente 12 mil palabras y que responda a preguntas basado en la información del PDF. Básicamente podría resumir el documento, obtener los puntos más importantes y mucho más.
Comando:Lambda [lee] el [pdf] y [preguntas sobre el pdf]
Ejemplo:Lambda lee el pdf y dame un resumen
Ejemplo:Lambda lee el pdf y dime la idea principal del texto
Ejemplo:Lambda lee el pdf y lista las palabras clave
"""