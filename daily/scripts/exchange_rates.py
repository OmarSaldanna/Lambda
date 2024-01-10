import os
import json

# data path
path = "/home/omarsaldanna/Lambda/daily/data/"
# env path
env_path = "/home/omarsaldanna/Lambda/.env"
# admited exchange rates
exchange_rates = ["MXN","CAD","USD","EUR","JPY"]

# clear the txt file
os.system(f'echo "" > {path}exchange_rates.txt')
# enable the api key
# and run the request and save it in a json
os.system(f'curl "http://api.exchangeratesapi.io/v1/latest?access_key=$exchangeapi" > {path}rates.json')
# open the .json file
data = json.load(open(f'{path}rates.json'))

# print the exchange rates on a txt
for rate in data['rates'].keys():
  # only the selected rates
  if rate in exchange_rates:  
    # print them inside an txt
    value = data['rates'][rate]
    os.system(f'echo "{rate}:{round(value,2)}" >> {path}exchange_rates.txt')


# remove the .json file
os.system(f"rm {path}rates.json")