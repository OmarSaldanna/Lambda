from core.modules import OpenAI


# lambda convierte
def main(params: tuple):
  # extract the params
  message, member, server = params
  # read the exchange_rates from lambda daily
  rates = ""
  with open('daily/data/exchange_rates.txt', 'r') as file:
    rates = file.read()
  # instance openai module
  openai = OpenAI(member, server)
  # try to make the answer shorter as possible
  message += f". Responde únicamente con el resultado, El tipo de cambio actual es:{rates}."
  # now call gpt
  return openai.gpt(message, system="Eres una IA capaz de hacer cálculos, considera que estás en México")


# info about the skill
info = """
### Exchange Trader
Es un conversor de monedas, por el momento solamente acepta las monedas: *Peso Argentino (ARS), Real Brasileño (BRL), Dólar Canadiense (CAD), Peso Chileno (CLP), Yuan Chino (CNY), Peso Colombiano (COP), Euro (EUR), Yen Japonés (JPY), Peso Mexicano (MXN), Sol Peruano (PEN), Dólar Estadounidense (USD) y Peso Uruguayo (UYU)*.
> **Comando:** Lambda intercambia ...
> **Ejemplo:** lambda intercambia 10 pesos a dolares
> **Ejemplo:** lambda intercambia 50 euroas a pesos mexicanos
"""