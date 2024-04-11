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

from clases import WeaponType, searchKey

path_serverIDS = r"C:\Users\ADM\AppData\Roaming\OTClientV8\AnenOTC\DumpIDS.json"
path_weaponsXML = r"D:\Documentos\BACKUP\BACKUP PC\TIBIA SERVER\Servidores\GLOBAL 10.00X13.30\global 1330\data\weapons\weapons.xml"


def readObjectsFile():
    with open("../DumpTibiaWiki/dumpObjects.json", 'r') as archivo:
        datos = json.load(archivo)
    return datos

# ITEMS XML
def readItemsXMLFile():
    global documentoXML
    documentoXML = etree.parse(path_weaponsXML, parser=etree.XMLParser(recover=True))
    return documentoXML.getroot()

weaponsXML = readItemsXMLFile()

def guardarXML():
    xml_string = etree.tostring(documentoXML, encoding='utf-8', xml_declaration=True, pretty_print=True)
    with open(path_weaponsXML, 'wb') as f:
        f.write(xml_string)
    print("weapons.xml sobreescrito")
    

    
archivo = readObjectsFile()


def createItemXML(data):
    elemento_item = etree.Element(data["weapontype"])
    elemento_item.append(etree.Comment(data["name"]))
    del data["weapontype"]
    del data["name"]
    for key, value in data.items():
        if key == 'vocations':
            # Si es el atributo "attributes", crear elementos hijos para cada atributo
            for atributo in value:
                elemento_atributo = etree.Element("vocation")
                elemento_atributo.set("name", str(atributo))
                elemento_item.append(elemento_atributo)
        else:
            # Si es otro atributo, establecerlo en el elemento item
            elemento_item.set(key, str(value))
            
    weaponsXML.append(elemento_item)

def searchItemById(id):
    return weaponsXML.xpath(f".//wand[@id='{id}']") or weaponsXML.xpath(f".//melee[@id='{id}']") or weaponsXML.xpath(f".//distance[@id='{id}']")


def getServerIDs():
    with open(path_serverIDS, "r") as archivo:
        return json.load(archivo)

serverIDs = getServerIDs()

def getServerId(id):
    return id and serverIDs.get(str(id)) or None

order = ["wand", "melee", "distance"]

def init():
    cont = 0
    items = []
    for infoItem in archivo:
        itemid = infoItem.get("itemid")
        objectclass = infoItem.get("objectclass")
        if itemid is None or objectclass is None or objectclass != "Weapons":
            continue
        itemid = itemid[0]
        item = {}
        item["id"] = getServerId(itemid)
        if item["id"] and len(searchItemById(item["id"])) == 0:
        
            
            weapon_type          = infoItem.get("weapontype") 
            primary_type         = infoItem.get("primarytype")
            damage_type          = infoItem.get("damagetype") 
            level_required       = infoItem.get("levelrequired")
            mana_cost            = infoItem.get("manacost")
            voc_required         = infoItem.get("vocrequired")
            damage_range         = infoItem.get("damagerange")
            name                 = infoItem.get("actualname") or infoItem.get("name")
            item["name"] = name
            item["weapontype"] = WeaponType.get(primary_type) or WeaponType.get(weapon_type)
            if item["weapontype"] is None:
                continue
            if level_required and level_required != "0":
                item["level"] = level_required
            if mana_cost:
                item["mana"] = mana_cost
            if voc_required:
                item["vocations"] = []
                vocs = re.finditer(r'(druids|sorcerers|knights|paladins)', voc_required)
                for coinci in vocs:
                    item["vocations"].append(coinci.group(1)[:-1].capitalize())
                if len(item["vocations"]) == 0:
                    del item["vocations"]
            if damage_range:
                coin = re.search(r"(\d+)-(\d+)", damage_range)
                item["min"] = coin.group(1)
                item["max"] = coin.group(2)
            if damage_type:
                item["type"] = damage_type.lower()
            else:
                item["unproperly"] = "1"
            
            # print(f"agg nuevo item CLIENT ID: {itemid}, SERVERID: {item['id']} ({name}) | {cont}")
            print(item)
            items.append(item)
            # createItemXML(item)
        else:
            print(f"ya existiendo, omitiendo {item['id']} | {cont}")
        cont += 1
    sorted_data = sorted(items, key=lambda x: order.index(x["weapontype"]))
    for item in sorted_data:  
        createItemXML(item)
    guardarXML()
init()

# print(len(searchItemById(None)))
