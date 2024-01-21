from core.modules import OpenAI


# traduce será un verbo de uso general
# lambda traduce al español Electricity rules the world
# lambda traduce al inglés La electricidad gobierna el mundo
def main(params: tuple):
  # extract the params
  message, member, server = params
  # instance openai module
  openai = OpenAI(member, server)
  # try to make the answer shorter as possible
  message += ". Responde únicamente con la traducción."
  # now call gpt
  return openai.gpt(message)


# info about the skill
info = """
Traductor
Es una función de Lambda que permite hacer traducciones al instante a casi cualquier idioma del mundo.
Comando 1:Lambda traduce el texto [texto a traducir]
Comando 2:Lambda [dime|dame] la traducción [texto a traducir]
Ejemplo:lambda traduce el texto Electricity rules the world
Ejemplo:lambda dame la traducción al inglés de La electricidad gobierna el mundo
"""