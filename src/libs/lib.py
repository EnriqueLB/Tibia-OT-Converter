from clases import Resist, Attrib, PrimaryType, SubPrimaryType, SlotType
import re

def cleanHit(texto):
    if not texto: 
        return None
            
    coincidencias = re.search(r"([+-]?\d+)", texto)
    if coincidencias:
        valor = coincidencias.group(1)
        if valor.startswith('-') or valor[0].isdigit():
            return {"key": "hitChance", "value": int(valor)}
        else:
            return {"key": "hitChance", "value": int(valor[1:])}

def cleanResist(texto):
    if not texto: 
        return None
    lista = []
        
    coincidencias = re.finditer(r'(fire|energy|ice|holy|death|drown|physical|earth|mana|life|drowning) (?:drain)?\s?([+-]?\d+)', texto)
    
    for coincidencia in coincidencias:
        habilidad = coincidencia.group(1)
        valor = coincidencia.group(2)            
        if valor[0].isdigit() or valor.startswith('-'):
            lista.append({"key": Resist[habilidad].value, "value": int(valor)})
        else:
            lista.append({"key": Resist[habilidad].value, "value": int(valor[1:])})
            
    return len(lista) > 0 and lista or None


def cleanAttrib(weight, texto, resist, hit_chance, attack, defense, imbueslots, description, armor, primary_type, slotType, secondary_type, rango, extra_def, duration, words, damagetype, crithit_ch, critextra_dmg, hpleech_am, hpleech_ch, volume):
    lista = []
    
    if texto:
        coincidencias = re.finditer(r'(distance|sword|club|axe|fist|magic|hard|invisibility|speed) (level|shield|fighting|drinking)?\s?([+-]\d+)?', texto)
    
        shield = re.search(r'shielding ([+-]\d+)', texto)
        
        if shield:
            valor = shield.group(1)
            if shield.group(1).startswith("-"):
                lista.append({"key": Attrib["shielding"].value, "value": int(valor)})
            else:
                lista.append({"key": Attrib["shielding"].value, "value": int(valor[1:])})

        for coincidencia in coincidencias:
            habilidad = coincidencia.group(1)
            tipo = coincidencia.group(2)
            valor = coincidencia.group(3)
            if habilidad == "hard" or habilidad == "invisibility":
                lista.append({"key": Attrib[habilidad].value, "value": 1})
            elif tipo == "shield":
                lista.append({"key": Attrib["magic_shield"].value, "value": 1})
            elif valor.startswith('-'):
                lista.append({"key": Attrib[habilidad].value, "value": int(valor)})
            else:
                lista.append({"key": Attrib[tipo == "level" and "magic_level" or habilidad].value, "value": int(valor[1:])})
    if weight:
        lista.append({"key": "weight", "value": int(weight.replace(".",""))})
    if resist:
        lista.extend(cleanResist(resist))
    if hit_chance:
        lista.append(cleanHit(hit_chance)) 
    if attack:
        lista.append({"key": "attack", "value": int(attack)})
    if imbueslots:
        lista.append({"key": "imbuingSlots", "value": int(imbueslots)})
    if defense:
        lista.append({"key": "defense", "value": int(defense)})
    if description:
        lista.append({"key": "description", "value": description})
    if armor:
        lista.append({"key": "armor", "value": int(armor)})
    if primary_type:
        res = cleanPrimaryType(primary_type)
        if res:
            lista.append(res)
    if slotType and re.search(r"two", slotType.lower()):
        lista.append({"key": "slotType", "value": "two-handed"})
    if secondary_type:
        res = cleanSecondarytype(secondary_type)
        if res:
            lista.append(res)
    if rango:
        res = re.search("(\d+)", rango)
        lista.append({"key": "range", "value": int(res.group(1))})
    if extra_def:
        lista.append({"key": "extradef", "value": int(extra_def)})
    if duration:
        tiempo = re.search(r'(\d+(\.\d+)?)', duration)
        tiempo = float(tiempo.group(1)) * 60
        lista.append({"key": "duration", "value": int(tiempo)})
    if words:
        lista.append({"key": "runeSpellName", "value": words})
    if damagetype:
        lista.append({"key": "shootType", "value": damagetype.lower()}) 
    if crithit_ch:
        lista.append({"key": "skillcriticalchance", "value": re.search(r"(\d+)",crithit_ch).group(1)}) 
    if critextra_dmg:
        lista.append({"key": "skillcriticaldamage", "value": re.search(r"(\d+)",critextra_dmg).group(1)}) 
    if hpleech_am:
        lista.append({"key": "skilllifeamount", "value": re.search(r"(\d+)", hpleech_am).group(1)}) 
    if hpleech_ch:
        lista.append({"key": "skilllifechance", "value": re.search(r"(\d+)", hpleech_ch).group(1)}) 
    if volume:
        lista.append({"key": "containerSize", "value": int(volume)}) 
        
    return len(lista) > 0 and lista or None

def cleanPrimaryType(texto):
    if not texto: 
        return None
    texto = texto.replace(" ", "_")
    
    
    #si es Furniture quiere decir que se tiene que separar multiples items e iterar los ids <attribute key="rotateTo" value="32020" />
    
    for tipo in SubPrimaryType:
        if re.search(tipo.name, texto):
            return {"key": "loottype", "value": tipo.value}
    
    for tipo in PrimaryType:
        if re.search(tipo.name, texto):
            if tipo.value == PrimaryType.Spellbooks.value:
                return {"key": "weaponType", "value": "shield"}
            elif tipo.value == PrimaryType.Wands.value:
                return {"key": "weaponType", "value": "wand"}
            else:
                return {"key": "weaponType", "value": tipo.value}
            
    for slotType in SlotType:
        if re.search(slotType.name, texto):
            return {"key": "slotType", "value": slotType.value}
    
def cleanSecondarytype(texto):
    if not texto: 
        return None
    if re.search("(Bows)", texto):
        return {"key": "ammoType", "value": "arrow"}
    elif re.search("(Crossbows)", texto):
        return {"key": "ammoType", "value": "bolt"}
    elif re.search("(Throwing)", texto):
        return {"key": "shootType", "value": "throwingknife"}
