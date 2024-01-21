from core.modules import OpenAI

def main(params: tuple):
  # extract the params
  message, member, server = params
  # instance openai module
  openai = OpenAI(member, server)
  # try to make the answer shorter as possible
  message += ". RESPONDE ÚNICAMENTE CON EL CÓDIGO COMENTADO."
  # now call gpt
  return openai.gpt(message)

# info about the skill
info = """
Programador
Lambda te escribirá programas basados en una descripción del programa, puede ser casi cualquier programa.
Comando 1:Lambda programa [descripción del programa]
Comando 2:Lambda [dame|crea|genera] un [codigo|programa|script|función|algoritmo] [descripción]
Ejemplo:Lambda programa un arduino para que haga parpadear a dos leds
Ejemplo:Lambda dame el código base HTML para una página web
"""