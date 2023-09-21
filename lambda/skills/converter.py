from core.modules import OpenAI


# lambda convierte
def main(params: tuple):
  # extract the params
  message, member, server = params
  # get only the message content
  # instance openai module
  openai = OpenAI(member, server)
  # try to make the answer shorter as possible
  message += ". Responde únicamente con el resultado."
  # now call gpt
  return openai.gpt(message, system="Eres una IA capaz de hacer cálculos")


# info about the skill
info = """
### Converter
Es un conversor universal de unidades, solo dile a que unidades o código quieres convertir algo y listo. **Este comando no aplica para conversiones a monedas**, para ese caso te recomiendo usar el comando **Intercambia**.
> **Comando:** Lambda convierte ...
> **Ejemplo:** Lambda convierte 111010110 a hexadecimal
> **Ejemplo:** lambda convierte 10 Kg a Libras
> **Ejemplo:** lambda convierte 124 Km a Millas
"""