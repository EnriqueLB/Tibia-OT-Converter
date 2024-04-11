import sys
import json
import requests
sys.path.append('../lib')

from clases import TibiaWiki

def getData(wiki):
    r = requests.get(f'https://tibiawiki.dev/api/{wiki.value}?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open(f"dump{wiki.name}.json", 'w') as archivo:
        json.dump(r.json(), archivo, indent=4)
    
    print(f"{wiki.value} dumped")
    

def dumpAll():
    for a in TibiaWiki:
        print(f"receiving {a.name}, wait few seconds")
        getData(a)


