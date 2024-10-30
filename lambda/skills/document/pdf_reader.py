import PyPDF2
from core.modules import OpenAI


def get_text_from_pdf(pdf_path: str):
  # create the PdfReader object
  pdf_file = PyPDF2.PdfReader(open(pdf_path, "rb"))
  # get the number of pages
  #num_pages = len(pdf_file.pages)
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


# 0   1  2   3  4 5
# lee el pdf de y dime ...
# lee el pdf de y dame ...
def main(params: tuple):
  # catch the params
  message, member, server = params
  # instance the OpenAI module
  openai = OpenAI(member, server)
  # first get the file id
  file_id = openai.user_data['file']
  # get the file path
  file_path = f'lambdrive/documents/{file_id}.pdf'
  # set a little context
  pdf_text = "Eres un asistente inteligente, respone basado en el contenido del archivo:\n"
  # try extract the text
  try:
    pdf_text += get_text_from_pdf(file_path)
  except:
    return [{
      "type": "error",
      "content": f"Lo siento <@{member}> no encontramos tu archivo, **subirlo de nuevo podría resolver esto.**"
    }]
  # check the text to have less tokens than 15,000. Since the question.
  token_count = openai.token_counter(pdf_text)
  if token_count > 15000:
    # then trow a warning that the text is too long
    return [{
      "type": "error",
      "content": f"Lo siento <@{member}> tu archivo excede el límite de palabras. Tu texto tiene {token_count} tokens."
    }]
  # then the file has an acceptable size
  # catch the question
  question = ' '.join(message.split(' ')[5:])
  # call OpenAI with an inicial message.
  return openai.gpt(question, model="gpt-3.5-turbo-16k", context=False, system=pdf_text)


# info about the skill
info = """
Lector de PDFs
Esta función permite que Lambda lea un archivo PDF de aproximadamente 12 mil palabras y que responda a preguntas basado en la información del PDF. Básicamente podría resumir el documento, obtener los puntos más importantes y mucho más.
Comando:Lambda [lee] el [pdf] y [preguntas sobre el pdf]
Ejemplo:Lambda lee el pdf y dame un resumen
Ejemplo:Lambda lee el pdf y dime la idea principal del texto
Ejemplo:Lambda lee el pdf y lista las palabras clave
"""