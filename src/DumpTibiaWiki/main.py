import requests
import sys
sys.path.append('../lib')

from clases import TibiaWiki

def getData(TibiaWiki):
    r = requests.get(f'https://tibiawiki.dev/api/{TibiaWiki.value}?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open(f"dump{TibiaWiki.value}.json", 'w') as archivo:
        json.dump(datos, archivo)

getData(TibiaWiki.Books)