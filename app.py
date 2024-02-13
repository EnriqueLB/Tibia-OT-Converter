
from lxml import etree
import os  
import requests
import re
import json
import logging
from lib import cleanAttrib
import datetime


nombre_archivo = "dumpInfo.txt"


def getObjetctItems():
    r = requests.get('https://tibiawiki.dev/api/objects?expand=true') # OBTENER LISTA COMPLETA DE ITEMS
    with open("dumpObjects.json", 'w') as archivo:
        json.dump(datos, archivo)


def readObjectsFile():
    with open("dumpObjects.json", 'r') as archivo:
        datos = json.load(archivo)
    return datos


archivo = readObjectsFile()


def saveItems(estructura):
    with open(nombre_archivo, "w") as archivo:
        for key, value in estructura.items():
            key_without_quotes = key.replace("'", "")
            
            archivo.write(f"{key_without_quotes} {value}\n")

    print("Archivo creado exitosamente.")

def init():
    cont = 0
    datos = {}
    for a in archivo:
        itemid = a.get("itemid")
        article = a.get("article")
        name = a.get("actualname") or a.get("name")
        if itemid is not None and name is not None:
            for id in itemid:
                if article is not None:
                    datos[str(id)] = article + " " + name.strip()
                else:
                    datos[str(id)] = name.strip()
        cont +=1
    saveItems(datos)
    
init()
