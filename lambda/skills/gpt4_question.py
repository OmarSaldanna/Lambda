from core.modules import OpenAI


# lambda pregunta a cuatro ...
# lambda dime con cuatro ...
# lambda responde con cuatro ...
# lambda contesta con cuatro ...
def main(params: tuple):
  # extract the params
  message, member, server = params
  # get only the message content
  words = message.split(' ')[3:]
  cut_message = ' '.join(words)
  # instance openai module
  openai = OpenAI(member, server)
  # try to make the answer shorter as possible
  message += ". Que tu respuesta sea concisa."
  # now call gpt
  return openai.gpt(cut_message, model="gpt-4")


# info about the skill
info = """
### GPT4 Conversation
Es básicamente la misma función que la conversación convencional, también almacena la conversación, el detalle es que **esta usa GPT4**, que es el modelo más capaz de OpenAI.
> **Comando:** Lambda [verbo] con cuatro ...
> **Ejemplo:** lambda dime con cuatro que son los agujeros negros
> **Ejemplo:** lambda pregunta a cuatro que es la radiación de Hawking
Los verbos disponibles son: **pregunta, dime, responde, contesta**.
"""