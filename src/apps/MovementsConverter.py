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

path_serverIDS = r"C:\Users\ADM\AppData\Roaming\OTClientV8\AnenOTC\DumpIDS.json"
path_movementsXML = r"D:\Documentos\BACKUP\BACKUP PC\TIBIA SERVER\Servidores\GLOBAL 10.00X13.30\global 1330\data\movements\movements.xml"


def readObjectsFile():
    with open("../DumpTibiaWiki/dumpObjects.json", 'r') as archivo:
        datos = json.load(archivo)
    return datos

# ITEMS XML
def readItemsXMLFile():
    global documentoXML
    documentoXML = etree.parse(path_movementsXML, parser=etree.XMLParser(recover=True))
    return documentoXML.getroot()

weaponsXML = readItemsXMLFile()

def guardarXML():
    xml_string = etree.tostring(documentoXML, encoding='utf-8', xml_declaration=True, pretty_print=True)
    with open(path_movementsXML, 'wb') as f:
        f.write(xml_string)
    print("movements.xml sobreescrito")
    

    
archivo = readObjectsFile()


def createItemXML(data, itemName = None):
    elemento_item = etree.Element("movevent")
    if itemName:
        elemento_item.append(etree.Comment(itemName))
    for key, value in data.items():
        if key == 'vocations':
            # Si es el atributo "attributes", crear elementos hijos para cada atributo
            for atributo in value:
                elemento_atributo = etree.Element("vocation")
                elemento_atributo.set("name", str(atributo))
                if re.search(r"(Master|Elder|Royal|Elite)", atributo):
                    elemento_atributo.set("showInDescription", "0")
                elemento_item.append(elemento_atributo)
        else:
            # Si es otro atributo, establecerlo en el elemento item
            elemento_item.set(key, str(value))
    #<movevent event="DeEquip" itemid="34067" slot="necklace" function="onDeEquipItem" />
    cierre = etree.Element("movevent")
    cierre.set("event", "DeEquip")
    cierre.set("itemid", str(data.get("itemid")))
    cierre.set("slot", data.get("slot"))
    cierre.set("function", "onDeEquipItem")
    weaponsXML.append(elemento_item)
    weaponsXML.append(cierre)

def searchItemById(id):
    return weaponsXML.xpath(f".//movevent[@itemid='{id}']") or weaponsXML.xpath(f".//movevent[@toid='{id}']") or weaponsXML.xpath(f".//movevent[@fromid='{id}']")


def getServerIDs():
    with open(path_serverIDS, "r") as archivo:
        return json.load(archivo)

serverIDs = getServerIDs()

def getServerId(id):
    return id and serverIDs.get(str(id)) or None



def init():
    for infoItem in archivo:
        itemid = infoItem.get("itemid")
        if itemid is None:
            continue
        itemid = itemid[0]
        item = {"event": "Equip", "itemid": getServerId(itemid)}
        
        if item["itemid"] and len(searchItemById(item["itemid"])) == 0:
        
            primary_type        = infoItem.get("primarytype") or ""
            hands               = infoItem.get("hands")
            name                = infoItem.get("actualname") or infoItem.get("name")
            level_required       = infoItem.get("levelrequired")
            voc_required        = infoItem.get("vocrequired")
            tipo = searchKey(primary_type.replace(" ", "_"), SlotType) or (hands and "hand" or None)
            
            if tipo is None:
                continue
            
            item["slot"] = tipo == "body" and "armor" or tipo

            if level_required and level_required != "0":
                item["level"] = level_required
                
            item["function"] = "onEquipItem"
            
            if voc_required:
                item["vocations"] = []
                vocs = re.finditer(r'(druids|sorcerers|knights|paladins)', voc_required)
                for coinci in vocs:
                    voc = coinci.group(1)[:-1].capitalize()
                    item["vocations"].append(voc)
                    if voc == "Druid":
                        item["vocations"].append("Elder Druid")
                    elif voc == "Sorcerer":
                        item["vocations"].append("Master Sorcerer")
                    elif voc == "Paladin":
                        item["vocations"].append("Royal Paladin")
                    else:
                        item["vocations"].append("Elite Knight")
                if len(item["vocations"]) == 0:
                    del item["vocations"]
            
            # print(f"agg nuevo item CLIENT ID: {itemid}, SERVERID: {item['id']} ({name}) | {cont}")
            print(item)
            createItemXML(item, name)
        # else:
        #     print(f"ya existiendo, omitiendo {item['itemid']}")

    guardarXML()
init()

# print(len(searchItemById(None)))
