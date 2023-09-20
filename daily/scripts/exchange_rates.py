from forex_python.converter import CurrencyRates
import os

path = "/home/omarsaldanna/Lambda/daily/data/"

def get_rounded_exchange_rates():
  # Create an instance of CurrencyRates
  c = CurrencyRates()

  # Define the currencies for which you want to obtain exchange rates
  currencies = ['EUR', 'IDR', 'BGN', 'GBP', 'DKK', 'CAD', 'JPY', 'HUF', 'RON', 'MYR', 'SEK', 'SGD', 'HKD', 'AUD', 'CHF', 'KRW', 'CNY', 'TRY', 'NZD', 'THB', 'USD', 'NOK', 'INR', 'MXN', 'CZK', 'BRL', 'PLN', 'PHP', 'ZAR']

  # Create a dictionary to store the rounded exchange rates
  exchange_rates = {}

  # Iterate through the currencies and get their exchange rates with respect to the US Dollar (USD)
  for currency in currencies:
    try:
      # Use the get_rate function to obtain the exchange rate
      rate = c.get_rate('USD', currency)

      # Round the exchange rate value to 2 decimal places
      rounded_rate = round(rate, 2)

      exchange_rates[currency] = rounded_rate
    except Exception as e:
      exchange_rates[currency] = None

  return exchange_rates

# Call the function to get the rounded exchange rates
rounded_rates = get_rounded_exchange_rates()

# clear the txt file
os.system(f'echo "" > {path}exchange_rates.txt')

# Print the rounded exchange rates
for currency, rate in rounded_rates.items():
  # print them inside an txt
  os.system(f'echo "{currency}:{rate}" >> {path}exchange_rates.txt')