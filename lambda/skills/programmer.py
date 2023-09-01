from core.modules import OpenAI

def main(params: tuple):
  # extract the params
  message, member, server = params
  # instance openai module
  openai = OpenAI(member, server)
  # try to make the answer shorter as possible
  message += ". Responde únicamente con el código."
  # now call gpt
  return openai.gpt(message)

# info about the skill
info = """
### Programmer 
Usas un modelo de lenguaje para poder escribir programas, literalmente **puedes pedirle a Lambda que te programe un Arduino, una página web, y muchas más cosas.**
> **Comando:** Lambda programa ...
> **Comando:** Lambda dame un [codigo o programa] ...
> **Ejemplo:** Lambda programa un arduino para que haga parpadear a dos leds
> **Ejemplo:** Lambda dame el código base HTML para una página web
Los verbos disponibles son: **programa, dame**.
"""