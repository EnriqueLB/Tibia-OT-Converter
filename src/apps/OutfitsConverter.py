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

from clases import SlotType, searchKey


path_outfitsXML = r"D:\Documentos\BACKUP\BACKUP PC\TIBIA SERVER\Servidores\GLOBAL 10.00X13.30\global 1330\data\xml\outfits.xml"


def readOutfitsFile():
    with open("../DumpTibiaWiki/dumpOutfits.json", 'r') as archivo:
        datos = json.load(archivo)
    return datos

# ITEMS XML
def readItemsXMLFile():
    global documentoXML
    documentoXML = etree.parse(path_outfitsXML, parser=etree.XMLParser(recover=True))
    return documentoXML.getroot()

outfitXML = readItemsXMLFile()

def guardarXML():
    xml_string = etree.tostring(documentoXML, encoding='utf-8', xml_declaration=True, pretty_print=True)
    with open(path_outfitsXML, 'wb') as f:
        f.write(xml_string)
    print("outfits.xml sobreescrito")
    

    
archivo = readOutfitsFile()


def createOutfitXML(data):
    elemento_item = etree.Element("outfit")
    for key, value in data.items():
        elemento_item.set(key, str(value))
        
    outfitXML.append(elemento_item)

def searchOutfitByName(name, male_id, female_id):
    return len(outfitXML.xpath(f".//outfit[@name='{name}']") +  outfitXML.xpath(f".//outfit[@looktype='{male_id}']")  + outfitXML.xpath(f".//outfit[@looktype='{female_id}']")) == 0

def init():
    for infoOutfit in archivo:
        
        name        = infoOutfit.get("name")
        female_id   = infoOutfit.get("female_id")
        male_id     = infoOutfit.get("male_id")
        premium     = infoOutfit.get("outfit")
        primary_type = infoOutfit.get("primarytype")
        bought      = infoOutfit.get("bought")
        unlocked = "yes"
        
        if not searchOutfitByName(name, male_id, female_id):
            continue
        
        if re.search(r"(Special|Quest)", primary_type) or (bought and bought == "yes"):
            unlocked = "no"
        outfit_female = {"type": "0", 
                "looktype": male_id,
                "name": name,
                "premium": premium == "free" and "no" or "yes",
                "unlocked": unlocked,
                "enabled": "yes"
                }
        
        outfit_male = {"type": "1", 
                "looktype": male_id,
                "name": name,
                "premium": premium == "free" and "no" or "yes",
                "unlocked": unlocked,
                "enabled": "yes"
                }
        print(f"Nuevo outfit ID: {male_id} , NAME: {name}")
        createOutfitXML(outfit_female)
        createOutfitXML(outfit_male)

    guardarXML()
init()

# print(len(searchItemById(None)))
