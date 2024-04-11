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


path_mountsXML = r"D:\Documentos\BACKUP\BACKUP PC\TIBIA SERVER\Servidores\GLOBAL 10.00X13.30\global 1330\data\xml\mounts.xml"


def readmountsFile():
    with open("../DumpTibiaWiki/dumpMounts.json", 'r') as archivo:
        datos = json.load(archivo)
    return datos

# ITEMS XML
def readMountsXMLFile():
    global documentoXML
    documentoXML = etree.parse(path_mountsXML, parser=etree.XMLParser(recover=True))
    return documentoXML.getroot()

mountXML = readMountsXMLFile()

#GET LAST ID
mount_elements = mountXML.xpath("//mount")
max_id = -1
for mount_element in mount_elements:
    id_value = int(mount_element.get("id"))
    if id_value > max_id:
        max_id = id_value

def guardarXML():
    xml_string = etree.tostring(documentoXML, encoding='utf-8', xml_declaration=True, pretty_print=True)
    with open(path_mountsXML, 'wb') as f:
        f.write(xml_string)
    print("monsters.xml sobreescrito")
    

    
archivo = readmountsFile()



def createMountXML(data):
    elemento_item = etree.Element("mount")
    for key, value in data.items():
        elemento_item.set(key, str(value))
        
    mountXML.append(elemento_item)

def searchMountByName(name, mount_id):
    return len(mountXML.xpath(f".//mount[@name='{name}']") + mountXML.xpath(f".//mount[@clientid='{mount_id}']")) == 0


def init(max_id):
    for infoMount in archivo:
        
        name        = infoMount.get("actualname") or infoMount.get("name")
        speed       = infoMount.get("speed")
        mount_id    = infoMount.get("mount_id")
        
        if not searchMountByName(name, mount_id):
            continue
        max_id += 1
        mount = {
            "id": max_id,
            "clientid": mount_id,
            "name" : name,
            "speed": speed,
            "premium": "yes"
        }

        print(f"Nuevo Mount ID: {mount_id} , NAME: {name}")
        createMountXML(mount)

    guardarXML()
init(max_id)

# print(len(searchItemById(None)))
