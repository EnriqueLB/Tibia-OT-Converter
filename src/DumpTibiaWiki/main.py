import requests




def getObjects():
    r = requests.get('https://tibiawiki.dev/api/objects?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)
        
def getBooks():
    r = requests.get('https://tibiawiki.dev/api/books?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)
        
def getAchievements():
    r = requests.get('https://tibiawiki.dev/api/achievements?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)
        
def getMounts():
    r = requests.get('https://tibiawiki.dev/api/mounts?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)
        
def getMissiles():
    r = requests.get('https://tibiawiki.dev/api/missiles?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)
        
def getEffects():
    r = requests.get('https://tibiawiki.dev/api/effects?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)
        
def getCharms():
    r = requests.get('https://tibiawiki.dev/api/charms?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)
        
def getNpcs():
    r = requests.get('https://tibiawiki.dev/api/npcs?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)
        
def getCreatures():
    r = requests.get('https://tibiawiki.dev/api/creatures?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)
        
def getBuildings():
    r = requests.get('https://tibiawiki.dev/api/creatures?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)
        
def getCreatures():
    r = requests.get('https://tibiawiki.dev/api/creatures?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)
        
        
