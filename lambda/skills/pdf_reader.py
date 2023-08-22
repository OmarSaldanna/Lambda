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


# 0   1  2   3   4 5    6
# lee el pdf $id y dime ...
# lee el pdf $id y dame ...
def main(params: tuple):
  # catch the params
  message, member, server = params
  # instance the OpenAI module
  openai = OpenAI(member, server)
  # first get the id
  file_id = message.split(' ')[3][1:]
  # get the file path
  file_path = f'lambdrive/documents/{file_id}.pdf'
  # set a little context
  text = "Responde a las preguntas basándote en la siguiente información:\n"
  # extract the text
  pdf_text += get_text_from_pdf(file_path)
  # check the text to have less tokens than 15,000. Since the question.
  if OpenAI.token_counter(text) > 15500:
    # then trow a warning that the text is too long
    return [{
      "type": "error",
      "content": f"Lo siento <@{member}> tu archivo excede el límite de palabras."
    }]
  # then the file has an acceptable size
  # catch the question
  question = ' '.join(message.split(' ')[:5])
  # call OpenAI with an inicial message.
  return openai.gpt(question, model="gpt-3.5-turbo-16k", context=False, system=pdf_text)


# info about the skill
info = """
### PDF Reader
Esta función permite que Lambda lea un archivo PDF de aproximadamente 12 mil palabras y que responda a preguntas basado en la información del PDF. Básicamente podría **resumir el documento, obtener los puntos más importantes hacer diagramas y mucho más**.
> **Comando:** Lambda lee el pdf **$id** y ...
> **Ejemplo 1:** Lambda lee el pdf $123ab y dame un resumen
> **Ejemplo 2:** Lambda lee el pdf $123ab y dime la idea principal del texto
> **Ejemplo 3:** Lambda lee el pdf $123ab y lista las palabras clave

"""