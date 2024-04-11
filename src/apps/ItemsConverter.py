"""
    ANEN
    V 1.0
    Obtiene los ultimos items de tibiwiki, y completa los items faltantes de tu items.xml
    Attributos no contemplados ya que no encontré forma de obtener esta informacion desde el api
		KEYS:
			type
			blockprojectile
			showattributes
			healthGain
			healthTicks
			manaGain
			manaTicks
			decayTo
			showduration
			transformDeEquipTo
			charges
			maxHitChance
			rotateTo
			wrapableTo
    Tome precaución, algunos nombres de item se pueden duplicar
"""


import os  
import requests
import re
import json
import logging
import sys
import datetime

from lxml import etree

sys.path.append('../libs')
sys.path.append('../DumpTibiaWiki')

from dumpper import getData
from lib import cleanAttrib
from clases import TibiaWiki

path_serverIDS = r"C:\Users\ADM\AppData\Roaming\OTClientV8\AnenOTC\DumpIDS.json"
path_itemsXML = r"D:\Documentos\BACKUP\BACKUP PC\TIBIA SERVER\Servidores\GLOBAL 10.00X13.30\global 1330\data\items\items.xml"


def readObjectsFile():
    if not os.path.exists("../DumpTibiaWiki/dumpObjects.json"):
        print("Objects file not exists, building...")
        getData(TibiaWiki.Objects)
        return
    
    with open("../DumpTibiaWiki/dumpObjects.json", 'r') as archivo:
        datos = json.load(archivo)
    return datos

# ITEMS XML
def readItemsXMLFile():
    global documentoXML
    documentoXML = etree.parse(path_itemsXML, parser=etree.XMLParser(recover=True))
    return documentoXML.getroot()

itemsXML = readItemsXMLFile()

def guardarXML():
    xml_string = etree.tostring(documentoXML, encoding='utf-8', xml_declaration=True, pretty_print=True)
    with open(path_itemsXML, 'wb') as f:
        f.write(xml_string)
    print("items.xml sobreescrito")
    

    
archivo = readObjectsFile()


def sortIDS(data):
    data.sort()
    listas = []
    sublista = [data[0]]

    try:
        for i in range(1, len(data)):
            checkData = re.search("(\d+)(?:\.|m)?\s(\d+)", data[i])
            if checkData:
                del data[i]
                data.append(checkData.group(1))
                data.append(checkData.group(2))
            if int(data[i]) - int(data[i-1]) == 1:
                sublista.append(data[i])
            else:
                listas.append(sublista)
                sublista = [data[i]]

        listas.append(sublista)
        return listas
    except Exception as e:
        print("Error, Data:", data)
        raise "Error:" + e
    


def createItemXML(data):
    elemento_item = etree.Element("item")
    for key, value in data.items():
        if key == 'attributes':
            # Si es el atributo "attributes", crear elementos hijos para cada atributo
            for atributo in value:
                elemento_atributo = etree.Element("attribute")
                for k, v in atributo.items():
                    elemento_atributo.set(k, str(v))
                elemento_item.append(elemento_atributo)
        else:
            # Si es otro atributo, establecerlo en el elemento item
            elemento_item.set(key, str(value))
    itemsXML.append(elemento_item)

def searchItemById(id):
    return itemsXML.xpath(f".//item[@id='{id}']") or itemsXML.xpath(f".//item[@fromid='{id}']")


def getServerIDs():
    with open(path_serverIDS, "r") as archivo:
        return json.load(archivo)

serverIDs = getServerIDs()

def getServerId(id):
    return id and serverIDs.get(str(id)) or None


def init():
    cont = 0
    datos = []
    if not archivo:
        return
    for infoItem in archivo:
        itemid = infoItem.get("itemid")
        if itemid is None:
            continue
        for lista in sortIDS(itemid):
            item = {}
            if len(lista) > 1:
                item["fromid"] = getServerId(lista[0])
                item["toid"] = getServerId(lista[len(lista)-1])
            else:
                item["id"] = getServerId(lista[0])
            if len(searchItemById(getServerId(lista[0]))) == 0:
                
                name                = infoItem.get("actualname") or infoItem.get("name")
                article             = infoItem.get("article")
                plural              = infoItem.get("plural")
                plural              = plural if re.search("\?", plural or "") is None else None
                attrib              = infoItem.get("attrib")
                weight              = infoItem.get("weight")
                description         = infoItem.get("flavortext")
                armor               = infoItem.get("armor")
                resis               = infoItem.get("resist")
                hit_chance          = infoItem.get("hit_mod")
                attack              = infoItem.get("atk_mod") or infoItem.get("attack")
                defense             = infoItem.get("defense")
                imbueslots          = infoItem.get("imbueslots")
                rango               = infoItem.get("range")
                extra_def           = infoItem.get("defensemod")
                duration            = infoItem.get("duration")
                words               = infoItem.get("words")
                damagetype          = infoItem.get("damagetype")
                crithit_ch          = infoItem.get("crithit_ch")
                critextra_dmg       = infoItem.get("critextra_dmg")
                hpleech_am          = infoItem.get("hpleech_am")
                hpleech_ch          = infoItem.get("hpleech_ch")
                volume              = infoItem.get("volume")
                
                hands = infoItem.get("hands")
                primary_type = infoItem.get("primarytype")
                secondary_type = infoItem.get("secondarytype")
                
                print(f"agg nuevo item CLIENT ID: {lista[0]}, SERVERID:{getServerId(lista[0])} ({name}) | {cont}")
                
                if article is not None:
                    item["article"] = article
                    
                item["name"] = name
                
                if plural is not None:
                    item["plural"] = plural
                    
                item["attributes"] = cleanAttrib(weight, attrib, resis, hit_chance, attack, defense, imbueslots, description, armor, primary_type, hands, secondary_type, rango, extra_def, duration, words, damagetype, crithit_ch, critextra_dmg, hpleech_am, hpleech_ch, volume)
                if item["attributes"] is None:
                    del item["attributes"]
                createItemXML(item)
                # datos.append(item)
            else:
                print(f"ya existiendo, omitiendo {getServerId(lista[0])} | {cont}")
            cont += 1
    guardarXML()
init()

# print(len(searchItemById(None)))
