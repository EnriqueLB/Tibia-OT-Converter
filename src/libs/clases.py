from enum import Enum

class Resist(Enum):
    fire        = "absorbPercentFire"
    energy      = "absorbPercentEnergy"
    holy        = "absorbPercentHoly"
    death       = "absorbPercentDeath"
    drown       = "absorbPercentDrown"
    drowning    = drown
    physical    = "absorbPercentPhysical"
    earth       = "absorbPercentEarth"
    ice         = "absorbPercentIce"
    mana        = "absorbPercentManaDrain"
    life        = "absorbPercentLifeDrain"  

class Attrib(Enum):
    distance        = "skillDist"
    shielding       = "skillShield"
    axe             = "skillAxe"
    sword           = "skillSword"
    club            = "skillClub"
    magic_level     = "magiclevelpoints"
    magic_shield    = "manashield"
    hard            = "suppressDrunk"
    invisibility    = "invisible"
    speed           = "speed"
    fist            = "skillFist"
        
class PrimaryType(Enum):
    Shields                 = "shield"
    Distance_Weapons        = "distance"
    Club_Weapons            = "club"
    Axe_Weapons             = "axe"
    Sword_Weapons           = "sword"
    Rods                    = "wand"
    Ammunition              = "ammunition"
    Spellbooks              = "spellbok"
    Wands                   = "wands"
    
class SubPrimaryType(Enum):
    Creature_Products       = "product"
    Decorations             = "decoration"
    Food                    = "food"
    Valuables               = "valuables"
    Liquids                 = "potion"

class SlotType(Enum): #SLOT TYPE PUEDE SER SI VIENE LA PROPIEDAD HANDS = TWO ENTONCES SLOTTYPE = TWO HANDED
    Amulets_and_Necklaces   = "necklace"
    Helmets                 = "head"
    Armors                  = "body"
    Boots                   = "feet"
    Legs                    = "legs"
    Containers              = "backpack"
    Light_Sources           = "ammo"
    Rings                   = "ring"
    
    

class TibiaWiki(Enum):
    Items               = "items"
    Books               = "books"
    Achievements        = "achievements"
    Mounts              = "mounts"
    Missiles            = "missiles"
    Effects             = "effects"
    Objects             = "objects"
    Charms              = "charms"
    Locations           = "locations"
    NPCs                = "npcs"
    Creatures           = "creatures"
    Buildings           = "buildings"
    Keys                = "keys"
    Loot_StatisticsV1   = "loot"
    Loot_StatisticsV2   = "v2/loot"
    Outfits             = "outfits"
    Hunting_Places      = "huntingplaces"
    Quests              = "quests"
    Streets             = "streets"
    Spells              = "spells"
    

WeaponType = {
    "Distance":         "distance",
    "Wands":            "wand",
    "Rods":             "wand",
    "Melee":            "melee",
    "Distance Weapons": "distance",
    "Ammunition":       "distance",
    "Club Weapons":     "melee",
    "Axe Weapons":      "melee",
    "Sword Weapons":    "melee",
    "Swords":           "melee",
    "Axe":              "melee",
    "Club":             "melee",
}

    
def searchKey(key, enum):
    if key is None:
        return
    for tipo in enum:
        if tipo.name == key:
            return tipo.value