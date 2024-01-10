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
  message += f". Responde UNICAMENTE con el resultado de la CONVERSIÓN y EL NOMBRE DE LA MONEDA, El tipo de cambio actual en EUROS es: {rates}."
  # now call gpt
  return openai.gpt(message, system="Eres una IA capaz de hacer cálculos, si solamente escribo 'pesos' me refiero a pesos mexicanos. HAZ UN CALCULO CORECTO.", context=False, model="gpt-4")


# info about the skill
info = """
### Exchange Trader
Es un conversor de monedas, por el momento solamente acepta las monedas: *Dólar Canadiense (CAD), Euro (EUR), Yen Japonés (JPY), Peso Mexicano (MXN), Dólar Estadounidense (USD)*.
> **Comando:** Lambda intercambia ...
> **Ejemplo:** lambda intercambia 10 pesos a dolares
> **Ejemplo:** lambda intercambia 50 euroas a pesos mexicanos
"""